config_bytes = [
	'distance_regulator',
	'rotation_regulator',
	'enable_stuck',
	'stuck',
	'debug',
	'status_change_report',
	'keep_count',
	'tmr',
	'motor_connected',
	'debug_encoders',
	'regulator_mode',
	'motor_flip_left',
	'motor_flip_right',

]
config_ints = [
	'stuck_distance_jump',
	'stuck_rotation_jump',
	'stuck_distance_max_fail_count',
	'stuck_rotation_max_fail_count',
	'motor_speed_limit',
	'left_motor_speed_limit',
	'right_motor_speed_limit',
	'motor_rate_of_change',
	'send_status_interval',
	'motor_const_roc',
	'tol1',
	'tol2',
	'version',

]
config_floats = [
	'wheel_distance',
	'wheel_r1',
	'wheel_r2',
	'pid_d_p',
	'pid_d_d',
	'pid_d_i',
	'pid_r_p',
	'pid_r_d',
	'pid_r_i',
	'accum_speed',
	'accum_clip',
	'vmax',
	'omega',
	'accel',
	'alpha',
	'slowdown',
	'slowdown_angle',
	'angle_speedup',
	'speed_drop',
	'encoder1',
	'encoder2',
	'encoder1_max',
	'encoder2_max',
	'setpoint1',
	'setpoint2',
	'speed1',
	'speed2',
	'pid_i1',
	'pid_i2',
	'pid_lin1',
	'pid_lin2',
	'kp',
	'ka',
	'kb',
]
commands = {
	'set_config': 'c',
	'get_config': 'C',
	'set_config_hash': 'h',
	'get_config_hash': 'H',
	'send_status_and_position': 'P',
	'unstuck': 'U',
	'motor': 'm',
	'keep_speed': 'M',
	'send_position': 'p',
	'set_speed': 'V',
	'set_rotation_speed': 'r',
	'relative_rotate': 'T',
	'absolute_rotate': 'A',
	'turn_and_go': 'G',
	'move_to': 'N',
	'curve': 'Q',
	'curve_relative': 'q',
	'diff_drive': 'L',
	'hard_stop': 'S',
	'motor_init': 'F',
	'soft_stop': 's',
	'smooth_stop': 't',
	'reset_driver': 'R',
	'kill_regulator': 'k',
	'forward': 'D',
	'forward_lazy': 'd',
	'set_position_and_orientation': 'I',
	'break': 'i',
	'linear_optocoupler': '-',
}
messages = {
	'debug_encoder1': '1',
	'debug_encoder2': '2',
	'send_status_and_position': 'P',
	'status_changed': 'p',
	'encoder1_ready': '!',
	'encoder2_ready': '@',
}

