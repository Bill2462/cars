from car import drive
from pygamepad.gamepads.default import Gamepad

def main():
    # Create gamepad instance
    gamepad = Gamepad()
    drive_controller = drive.DriveController()
    print("Ready!")
    gamepad.listen()

    try:
        while True:
            dpad_x = -float(gamepad.buttons.ABS_HAT0X.value)
            dpad_y = -float(gamepad.buttons.ABS_HAT0Y.value)

            print("D-pad axes: ({}, {})".format(dpad_x, dpad_y))
            
            if dpad_y > 0:
                dpad_y = 0.2
            if dpad_y < 0:
                dpad_y = -0.5
            
            drive_controller.drive(dpad_y, dpad_x, 0.1)

    except KeyboardInterrupt:
        gamepad.stop_listening()
        drive_controller.stop_car()

if __name__ == "__main__":
    main()
