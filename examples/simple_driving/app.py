from car.drive import NvidiaRacecar
from time import sleep

drive = NvidiaRacecar()

def main():
    drive.steering = 1.0
    sleep(1)
    drive.steering = -1.0
    sleep(1)
    drive.steering = 0.0

    drive.throttle = 0.2

    sleep(0.5)
    drive.throttle = -0.2
    sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except Exception as _:
        drive.stop()
    drive.stop()
