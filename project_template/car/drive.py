import zmq
import time

def _time_ms():
    return time.time_ns() // 1_000_000

class DriveController:
    def __init__(self, command_address="tcp://*:5555",
                 command_topic="motor_commands"):
        context = zmq.Context()
        self.command_socket = context.socket(zmq.PUB)
        self.command_socket.bind(command_address)
        self.command_topic = command_topic

        time.sleep(2)
        self.last_command = _time_ms()

    def send_command(self, throttle, steering, duration, blocking=True):
        if self.is_command_running():
            raise Exception("Last command is still executing!")

        self.socket.send_string(self.topic, zmq.SNDMORE)
        self.socket.send_pyobj({
            "throttle": float(throttle),
            "steering": float(steering),
            "duration": float(duration)
        })

        if blocking:
            time.sleep(duration)
            return

        self.last_command = _time_ms() + duration*1e3

    def clear_error(self):
        self.send_command("CLEAR_ERROR", 0, 0)

    def is_command_running(self):
        return self.last_command > _time_ms()

    def stop_car(self):
        self.send_command(0, 0, 0.01)
