from car.drive import Car
from car.keyboard import Keyboard
import time

drive_controller = Car()
drive_controller.steering_offset = 0.0 # Ustaw tutaj wartość offsetu sterowania ustaloną w zadaniu z podstawami sterowania.

def main():

    # Obiekt keyboard będzie nasłuchiwał wydarzeń z klawiatury i zwracał stan klawiszy.
    keyboard = Keyboard()
    keyboard.start_listening()

    while 1:
        # Aktualny stan klawiszy możemy odczytać z atrybutów keyboard.UP, keyboard.DOWN, keyboard.LEFT, keyboard.RIGHT.
        # Obiekt keyboard zawiera 4 attrybuty które odpowiadają staną klawiszy strzałek.
        # Jeżeli klawisz jest wciśnięty to atrybut będzie miał wartość True, w przeciwnym wypadku False.

        # Przykład który wyświetla stan klawiszy w konsoli.
        # print(keyboard.UP, keyboard.DOWN, keyboard.LEFT, keyboard.RIGHT)

if __name__ == "__main__":
    # Jeśli wystąpi błąd to go wyświetl i zatrzymaj silniki.
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
