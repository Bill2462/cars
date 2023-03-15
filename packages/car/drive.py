import time
from .misc import time_ms
from .pub import ZmqPublisher

class DriveController:
    def __init__(self, address="tcp://*:5555",
                 topic="motor_commands"):
        self.pub = ZmqPublisher(address)
        self.topic = topic

        self.last_command = time_ms()

    def send_command(self, throttle, steering, duration, blocking=True):
        if self.is_command_running():
            raise Exception("Last command is still executing!")

        self.pub.send(self.topic, (time_ms(), {
            "throttle": float(throttle),
            "steering": float(steering),
            "duration": float(duration)
        }))

        if blocking:
            time.sleep(duration)
            return

        self.last_command = time_ms() + duration*1e3

    def is_command_running(self):
        return self.last_command > time_ms()

    def stop_car(self):
        self.send_command(0, 0, 0.01)
