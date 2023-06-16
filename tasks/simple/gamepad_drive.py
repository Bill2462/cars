from car.drive import Car
from car.pad import PadController

drive_controller = Car()
gamepad = PadController()

def correct_steering(x, offset=0.0, gain=1.0):
    return x*gain + offset

def main():

    while True:
        x, y = gamepad.get_control()

        # Przepisz offset z poprzedniego zadania. Zmodyfikuj gain i wartości throttle do jazdy do przodu
        # i do tyłu tak aby łazikiem się wygodnie sterowało.
        if y > 0:
            drive_controller.throttle = 0.0
        if y < 0:
            drive_controller.throttle = -0.0
        
        drive_controller.steering = correct_steering(x, offset=0.0, gain=1.0)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
        gamepad.stop_listening()
