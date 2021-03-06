import sys,socket,struct,time
from com.conf_can import *
from util.Convert import *
from conf import *

class Can:

	def __init__(self, addr=0, debug=0):
		self.addr = addr
		self.can_frame_fmt = "=IB3x8s"
		self.use_eff = 0x80000000
		self.debug = debug
		self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
		iface = can_dev
		self.s.bind((iface,))
		
	def ext(self, tf):
		if tf:
			self.use_eff = 0x80000000
		else:
			self.use_eff = 0
	
	def init():
		import subprocess
		subprocess.call('sudo ip link set can0 down'.split(' '))
		subprocess.call('sudo ip link set can0 up type can bitrate 500000 restart-ms 10'.split(' '))

	def _build_can_frame(self, can_id, data):
			can_dlc = len(data)
			data = data.ljust(8, b'\x00')
			return struct.pack(self.can_frame_fmt, can_id | self.use_eff, can_dlc, data)

	def _dissect_can_frame(self,frame):
			can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, frame)
			return (can_id, can_dlc, data[:can_dlc])

	def swap32(i):
			return struct.unpack('<I', struct.pack('>I', i))[0]

	def set_addr(self, a):
		self.addr = a
		
	def send(self, binary, addr=None):
		
		def _send(binary, addr=None):
			if addr == None: addr = self.addr
			frame = self._build_can_frame(addr, binary)
			if self.debug: print('[debug] sent: ' + nice_hex(binary))
			self.s.send(frame)
		
		# if bigger than 8 bytes, send by using CAN packet extender protocol
		if len(binary) > 8:
			left = len(binary) - 1
			s = 1
			# \rTL 5
			l =  min(left,5)
			_send(b'\n' + bytes([binary[0], left]) + binary[s:s+l], addr)
			left -= l
			s += l
			while left > 0:
				l =  min(left,7)
				_send(b'\r'+binary[s:s+l], addr)
				# print(s,left)
				left -= l
				s += l
		else:
			# send normal packet
			_send(binary, addr)
	
		
	def read(self, addr=None):
		while True:
			frame = self._dissect_can_frame(self.s.recv(16))
			if addr == None:
				return (hex(frame[0]), frame[2])
			elif addr | 0x80000000 == frame[0] or addr == frame[0]:
				return frame[2]
				
		
	def send_frame(self,f,val,addr=None):
		''' 
		format, values
		'''
		frame = self._build_can_frame(addr, struct.pack(f, *val))
		if self.debug: print('[debug] sent: ' + nice_hex(frame))
		self.s.send(frame)

	def read_frame(self):
		frame = self._dissect_can_frame(self.s.recv(16))
		if self.debug: print(nice_hex(frame[2]))
		return frame


	# servo and actuators (could be moved to other file maybe)
	def servo(self,which,f,val=None,addr=None):
		
		if f not in servo_commands:        
			print('function ' + f + ' doesn\'t exist')
			return

		if type(which) is str:
			if which not in robot_servos:
				print('servo ' + which + ' doesn\'t exist')
				return
			servo = robot_servos[which]
			servo_id = servo[1]
		elif type(which) is int:
			servo_id = which
		
		cmd = servo_commands[f]
		servo_len = 4
		servo_func = cmd[0]
		servo_rw = cmd[1]
		pfmt=servo_fmt = cmd[2]

		if val == None and 'R' not in servo_rw:
			print('function ' + f + ' is not readable')
			return

		if val != None and 'W' not in servo_rw:
			print('function ' + f + ' is not writable')
			return

		if val == None:
			servo_rw = 2
			servo_fmt = 'B'
			servo_len = 4
		else:
			servo_rw = 3
			if servo_fmt == 'h':
				servo_len += 1

		if addr == None:
			addr = 0x7f00 if type(which) is int or servo[0] == 'ax' else 0x7f01
		fmt = '4B'+servo_fmt
		data = [servo_id, servo_len, servo_rw, servo_func]
		if val != None:
			data += [val]
		else:
			data += [2] if pfmt == 'h' else [1]

		self.send_frame(fmt, data, addr)
		
		# handle reading
		#TODO: make it work
		'''
		if val == None:
			print('Sent request, waiting for answer')
			while True:
				frame = self.read_frame()
				
				if frame[0] == (addr | self.use_eff) and frame[1] > 0:
					print(hex(frame[0]), nice_hex(frame[2]))
					return
		'''

	def actuator(self, which, val=None):
		'''
			which - which actuator to send data to
			val - value to write
				(omitt if reading sensor)
		'''
		
		if type(which) is int:
			self.raw(which, 'B', [val])
		else:
			if which not in robot_byte_act:
				print('sensor or actuator ' + which + ' doesn\'t exist')
				return

			act = robot_byte_act[which]

			if val != None and 'W' not in act[1]:
				print('Cannot write to sensor')
			
			if val == None and 'R' not in act[1]:
				print('Cannot read from actuator')

			data = []
			if val != None:
				data = [val]
			else:
				print("reading from sensor not implemented yet")

			self.send_frame(act[0], 'B', [val])
		
