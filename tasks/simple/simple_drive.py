from car.drive import Car
from time import sleep

drive_controller = Car()

def correct_steering(x, offset=0.0, gain=1.0):
    return x*gain + offset

def main():
    # Instrukcje do sterowania autem które wykonają się tylko raz.
    # Przykładowy kod do jazdy.
    drive_controller.throttle = 0.2
    drive_controller.steering = correct_steering(0.0, offset=0.0)
    sleep(1)
    drive_controller.throttle = 0
    drive_controller.steering = correct_steering(1.0, offset=0.0)
    sleep(1)
    drive_controller.throttle = -0.3
    drive_controller.steering = correct_steering(-1.0, offset=0.0)
    sleep(1)
    drive_controller.throttle = 0
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
