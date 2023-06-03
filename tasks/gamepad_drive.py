from car.drive import Car
from pygamepad.gamepads.default import Gamepad

car = Car()
gamepad = Gamepad()

def main():
    gamepad.listen()

    # Tu wpisz kod który wykona się tylko raz.

    while True:
        # Kod w pętli tu wpisz kod!
        pass # Usuń tę linię

if __name__ == "__main__":
    try:
        main()
    except Exception as _:
        car.stop()
        gamepad.stop_listening()
