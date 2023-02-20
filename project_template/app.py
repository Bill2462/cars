from car import drive
from time import sleep

def main():
    drive_controller = drive.DriveController()
    drive_controller.send_command(1.0, 0, 2)
    drive_controller.stop_car()
    sleep(1)
    drive_controller.send_command(-1.0, 0.3, 1)
    drive_controller.stop_car()
    sleep(1)


if __name__ == "__main__":
    main()
