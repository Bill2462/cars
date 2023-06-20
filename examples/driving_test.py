from car.drive import Car
from time import sleep

drive_controller = Car()

def main():
    drive_controller.steering = 1.0
    sleep(1)
    drive_controller.steering = -1.0
    sleep(1)
    drive_controller.steering = 0.0

    drive_controller.throttle = 0.2

    sleep(0.5)
    drive_controller.throttle = -0.2
    sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
