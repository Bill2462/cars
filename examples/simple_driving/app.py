from car import drive
from time import sleep

def main():
    drive_controller = drive.DriveController()
    print("Ready!")
    
    drive_controller.drive(0.1, 0.0, 0.5)
    drive_controller.stop_car()
    sleep(1)
    drive_controller.drive(-1.0, 0.0, 0.5)
    drive_controller.stop_car()
    sleep(1)

if __name__ == "__main__":
    main()
