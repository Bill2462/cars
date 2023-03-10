from car import drive
from car.telemetry import Telemetry
from car.camera import CSICamera
from time import sleep

def main():
    tm = Telemetry()
    cam = CSICamera(21, 3280, 2464, 512, 512)
    drive_controller = drive.DriveController()
    drive_controller.send_command(1.0, 0, 2)
    drive_controller.stop_car()
    sleep(1)
    drive_controller.send_command(-1.0, 0.3, 1)
    drive_controller.stop_car()
    sleep(1)

    while 1:
        img = cam.read()
        tm.log_image("cam", img)

if __name__ == "__main__":
    main()
