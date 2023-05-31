from car.drive import Car
from pygamepad.gamepads.default import Gamepad

car = Car()
gamepad = Gamepad()

def main():
    print("Ready!")
    gamepad.listen()

    while True:
        dpad_x = -float(gamepad.buttons.ABS_HAT0X.value)
        dpad_y = -float(gamepad.buttons.ABS_HAT0Y.value)

        print("D-pad axes: ({}, {})".format(dpad_x, dpad_y))

        if dpad_y > 0:
            dpad_y = 0.3
        if dpad_y < 0:
            dpad_y = -0.3

        car.steering = dpad_x
        car.throttle = dpad_y

if __name__ == "__main__":
    try:
        main()
    except Exception as _:
        car.stop()
        gamepad.stop_listening()
