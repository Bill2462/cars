from car.drive import Car
from car.pad import PadController
import time

drive_controller = Car()
drive_controller.steering_offset = 0.1 # Ustaw tutaj wartość offsetu sterowania ustaloną w zadaniu z podstawami sterowania.

# Obiekt gamepad będzie nasłuchiwał wydarzeń z kontrolera gier i zwracał kontrolek.
gamepad = PadController()

def main():
    print("Ready!")

    while True:
        # Aktualny stan kontroler kontrolera gier można otrzymać za pomocą metody get_control().
        x, y = gamepad.get_control()

        # Zmienna X odpowiada strzałkom w lewo i prawo.
        # Zmienna Y odpowiada strzałkom góra i dół.
        # Wartości zmiennych x i y są z przedziału od -1 do 1.
        # Wartość 0 oznacza że klawisz nie jest wciśnięty.
        # 
        # Dla X wartość 1 oznacza że prawa strzałka jest wciśnięta. Wartość -1 oznaacza że lewa strzałka jest wciśnięta.
        # Dla Y wartość 1 oznacza że strzałka góra jest wciśnięta. Wartość -1 oznaacza że strzałka dół jest wciśnięta.

        # Przykładowy kod który ustawia napęd i kierunek w zależności od stanu zmiennej y i x. 
        # x i y muszą być zmiennymi typu float i muszą być stworzone wcześniej.

if __name__ == "__main__":
    # Jeśli wystąpi błąd to go wyświetl i zatrzymaj silniki.
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
        gamepad.stop_listening()