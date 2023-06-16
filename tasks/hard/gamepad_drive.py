from car.drive import Car
from car.pad import PadController

drive_controller = Car()
gamepad = PadController()

def main():

    while True:
        x, y = gamepad.get_control()
        print(x, y)

        # Dodaj kod do kontroli auta.
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
        gamepad.stop_listening()
