from car.drive import Car
from car.keyboard import Keyboard
import time

drive_controller = Car()

def main():
    keyboard = Keyboard()
    keyboard.start_listening()

    while 1:
        print(keyboard.UP, keyboard.DOWN, keyboard.LEFT, keyboard.RIGHT)

        if keyboard.UP:
            y = 0.2
        elif keyboard.DOWN:
            y = -0.3
        else:
            y = 0
        
        if keyboard.LEFT:
            x = -0.3
        elif keyboard.RIGHT:
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
