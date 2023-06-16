from car.drive import Car
from time import sleep

drive_controller = Car()

def main():
    # Instrukcje do sterowania autem które wykonają się tylko raz.
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
