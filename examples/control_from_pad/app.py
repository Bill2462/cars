from car.drive import Car
from car.pad import PadController

drive_controller = Car()
gamepad = PadController()

def main():
    print("Ready!")

    drive_controller.steering_offset = 0.1

    while True:
        x, y = gamepad.get_control()

        if y > 0:
            y = 0.25
        if y < 0:
            y = -0.3

        drive_controller.steering = x
        drive_controller.throttle = y

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
        gamepad.stop_listening()
