from adafruit_servokit import ServoKit
from time import sleep
import traitlets

class Racecar(traitlets.HasTraits):
    steering = traitlets.Float()
    throttle = traitlets.Float()

    @traitlets.validate('steering')
    def _clip_steering(self, proposal):
        if proposal['value'] > 1.0:
            return 1.0
        elif proposal['value'] < -1.0:
            return -1.0
        else:
            return proposal['value']

    @traitlets.validate('throttle')
    def _clip_throttle(self, proposal):
        if proposal['value'] > 1.0:
            return 1.0
        elif proposal['value'] < -1.0:
            return -1.0
        else:
            return proposal['value']

class NvidiaRacecar(Racecar):
    i2c_address = traitlets.Integer(default_value=0x40)
    steering_gain = traitlets.Float(default_value=-0.65)
    steering_offset = traitlets.Float(default_value=0)
    steering_channel = traitlets.Integer(default_value=0)
    throttle_gain = traitlets.Float(default_value=0.8)
    throttle_channel = traitlets.Integer(default_value=1)

    def __init__(self, *args, **kwargs):
        super(NvidiaRacecar, self).__init__(*args, **kwargs)
        self.kit = ServoKit(channels=16, address=self.i2c_address)
        self.steering_motor = self.kit.continuous_servo[self.steering_channel]
        self.throttle_motor = self.kit.continuous_servo[self.throttle_channel]

        self.last_motor_value = 1

    def stop(self):
        self.steering = 0.0
        self.throttle = 0.0

    @traitlets.observe('steering')
    def _on_steering(self, change):
        self.steering_motor.throttle = change['new'] * self.steering_gain + self.steering_offset

    @traitlets.observe('throttle')
    def _on_throttle(self, change):

        # Sequence to enable driving backwards (Why is this needed  WTF is this drive controller?)
        sign = lambda x: (1, -1)[x<=0]
        if sign(change['new']) == -1 and sign(self.last_motor_value) == 1:
            self.throttle_motor.throttle = 0.0
            sleep(0.2)
            self.throttle_motor.throttle = -0.3
            sleep(0.2)
            self.throttle_motor.throttle = 0.0
            sleep(0.2)

        self.throttle_motor.throttle = change['new'] * self.throttle_gain
        self.last_motor_value = change['new']
