from car.drive import Car
from car.keyboard import Keyboard
import time

drive_controller = Car()

def main():
    Keyboard = Keyboard()
    Keyboard.start_listening()

    while 1:
        print(Keyboard.UP, Keyboard.DOWN, Keyboard.LEFT, Keyboard.RIGHT)

        if Keyboard.UP:
            y = 0.2
        elif Keyboard.DOWN:
            y = -0.3
        else:
            y = 0
        
        if Keyboard.LEFT:
            x = -0.3
        elif Keyboard.RIGHT:
            x = 0.3
        else:
            x = 0
        
        drive_controller.throttle = y
        drive_controller.steering = x

        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()