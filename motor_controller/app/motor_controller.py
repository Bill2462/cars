import time
from adafruit_servokit import ServoKit

class InvalidCommandValue(Exception):
    pass

class MotorCommand:
    def __init__(self, throttle_setting, steering_setting, duration):
        self.throttle_setting = self._validate_type(throttle_setting, float, "throttle_setting")
        self.steering_setting = self._validate_type(steering_setting, float, "steering_setting")
        self.duration = self._validate_type(duration, float, "duration")

    def _validate_type(self, value, required_type, value_name):
        if not isinstance(value, required_type):
            raise InvalidCommandValue(f"{value_name} has wrong type! Got {type(value)}, require {required_type}.")
        return value

class MotorController:
    def __init__(self, config: dict):
        self.kit = ServoKit(channels=16, address=0x40)
        self.steering_motor = self.kit.continuous_servo[0]
        self.throttle_motor = self.kit.continuous_servo[1]

        steering_config = config["steering"]
        self.steering_gain = steering_config["gain"]
        self.steering_offset = steering_config["offset"]
        
        throttle_config = config["throttle"]
        self.throttle_negative_gain = throttle_config["negative_gain"]
        self.throttle_positive_gain = throttle_config["positive_gain"]

        self.throttle_negative_offset = throttle_config["negative_offset"]
        self.throttle_positive_offset = throttle_config["positive_offset"]

        self.max_command_duration = config["max_command_duration"]

        self.current_steering_motor = 0.0
        self.set_steering(0)

    def execute_command(self, cmd: MotorCommand):
        def cap(value, min, max):
            if value < min:
                return min
            if value > max:
                return max
            return value
        
        if cmd.duration < 0:
            raise InvalidCommandValue(f"Duration is must be > 0. Got {cmd.duration}")
        if cmd.duration > self.max_command_duration:
            raise InvalidCommandValue(f"Max command duration ({self.max_command_duration}) exceeded. Got {cmd.duration}")
        
        self.set_steering(cap(cmd.steering_setting, -1, 1))
        self.set_throttle(cap(cmd.throttle_setting, -1, 1))

        time.sleep(cmd.duration)
        self.throttle_motor.throttle = 0

    def set_steering(self, value: float):
        self.steering_motor.throttle = self.steering_gain*value + self.steering_offset

    def set_throttle(self, value: float):
        if value < 0:
            offset = self.throttle_negative_offset
            gain = self.throttle_negative_gain
        else:
            offset = self.throttle_positive_offset
            gain = self.throttle_positive_gain

        # Fucking magic to unlock driving backwards.
        # It does not work without this magic sequence xd.
        sign = lambda x: (1, -1)[x<0]
        if sign(value) == -1 and sign(self.current_steering_motor) > 0:
            self.throttle_motor.throttle = 0
            time.sleep(0.2)
            self.throttle_motor.throttle = -0.3
            time.sleep(0.2)
            self.throttle_motor.throttle = 0
            time.sleep(0.2)

        new_value = value*gain + offset
        self.throttle_motor.throttle = new_value
        self.current_steering_motor = new_value
