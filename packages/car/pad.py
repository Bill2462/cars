from pygamepad.gamepads.default import Gamepad

class PadController:
    def __init__(self) -> None:
        self.gamepad = Gamepad()
        self.gamepad.listen()
    
    def get_control(self):
        dpad_x = float(self.gamepad.buttons.ABS_HAT0X.value)
        dpad_y = -float(self.gamepad.buttons.ABS_HAT0Y.value)
        return dpad_x, dpad_y
    
    def disconnect(self) -> None:
        self.gamepad.stop_listening()
    
