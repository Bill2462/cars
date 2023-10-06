from car.drive import Car
from car.pad import PadController
import time

# NOTATKA: Kod powinien być uruchomiony jako root.
# Komenda to uruchomienia programu to: sudo python3 control_from_pad.py

drive_controller = Car()
STEERING_OFFSET = 0.1 # Ustaw tutaj wartość offsetu sterowania ustaloną w zadaniu z podstawami sterowania.

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

        # Przykładowy kod który ustawia zmienną w zależności od stanu klawiszy UP i DOWN.
        # if y > 0:
        #     y = 0.25
        # if y < 0:
        #     y = -0.3

        # Notatka: wartość x powinna być przeskalowana w dół z zakresu <1, -1> na mniejszy zakres.
        # Inaczej łazikiem będzie się ciężko sterowało bo będzie skręcał bardzo gwałtownie.

        # Przykładowy kod który ustawia napęd i kierunek w zależności od stanu zmiennej y i x. 
        # x i y muszą być zmiennymi typu float i muszą być stworzone wcześniej.

        drive_controller.throttle = 0.0 # UWAGA; nie dawaj tutaj surowej wartości y bo łazik pojedzie bardzo szybko.
        drive_controller.steering = x + STEERING_OFFSET

        # Co ile sekund mamy zaktualizować stan silników.
        # To musi tu zostać bo inaczej mogą wystąpić problemy z komunikacją z kontrolerem PWM.
        time.sleep(0.1)

if __name__ == "__main__":
    # Jeśli wystąpi błąd to go wyświetl i zatrzymaj silniki.
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
        gamepad.stop_listening()
