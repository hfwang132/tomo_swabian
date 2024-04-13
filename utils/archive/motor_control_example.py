# This file is created by Haifei

from pylablib.devices import Thorlabs

# >>> Thorlabs.list_kinesis_devices()
# [('83855348', 'APT DC Motor Controller'), ('83854828', 'APT DC Motor Controller')]

stage = Thorlabs.KinesisMotor("83855348")

# >>> stage.get_scale()
# (1, 22.369621333333335, 0.007635497415111112) # position, velocity, acceleration
# >>> stage.get_scale_units()
# 'step'

# >>> stage.get_position()
# >>> stage.move_by(distance=1)
# >>> stage.get_position()
# 2
# >>> stage.move_to(-1)
# >>> stage.get_position()
# 1
# >>> stage.get_position()
# -1
# >>> stage.wait_for_stop()

# 3455 step = 0.1 mm
# 34555 steps = 1 mm