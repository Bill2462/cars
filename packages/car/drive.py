import time
from adafruit_servokit import ServoKit

class DriveController:
    def __init__(self,
                 steering_gain = 1.0,
                 steering_offset = 0.0,
                 throttle_negative_gain = 0.12,
                 throttle_positive_gain = 0.04,
                 throttle_negative_offset = -0.15,
                 throttle_positive_offset = 0.2,
                 dummy=True):

        if not dummy:
            self.kit = ServoKit(channels=16, address=0x40)
            self.steering_motor = self.kit.continuous_servo[0]
            self.throttle_motor = self.kit.continuous_servo[1]

        self.steering_gain = steering_gain
        self.steering_offset = steering_offset

        self.throttle_negative_gain = throttle_negative_gain
        self.throttle_positive_gain = throttle_positive_gain
        self.throttle_negative_offset = throttle_negative_offset
        self.throttle_positive_offset = throttle_positive_offset
        self.dummy = dummy

    def drive(self, throttle: float, steering: float, duration: float):
        def cap(value, min, max):
            if value < min:
                return min
            if value > max:
                return max
            return value

        throttle = cap(throttle, -1, 1)
        steering - cap(steering, -1, 1)

        if self.dummy:
            print(f"Throttle: {throttle}    steering: {steering}")
        else:
            self.set_steering(steering)
            self.set_throttle(throttle)

        time.sleep(duration)

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
        sign = lambda x: (1, -1)[x<=0]
        if sign(value) == -1 and sign(self.current_steering_motor) > 0:
            self.throttle_motor.throttle = 0
            time.sleep(0.2)
            self.throttle_motor.throttle = -0.3
            time.sleep(0.2)
            self.throttle_motor.throttle = 0
            time.sleep(0.2)


        if value < 0.0001 and value > -0.001:
            new_value = 0
        else:
            new_value = value*gain + offset
        
        self.throttle_motor.throttle = new_value
        self.current_steering_motor = new_value
    
    def stop_car(self):
        self.drive(0, 0, 0.01)
