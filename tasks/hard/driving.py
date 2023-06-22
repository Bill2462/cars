from car.drive import Car
from time import sleep

drive_controller = Car()

# Podczas kalibracji steering_offset zostaw oryginalny kod który jedzie do przodu i do tyłu i 
# powoli zmieniaj ta wartość tak aby łazik jechał prosto.
drive_controller.steering_offset = 0.0 # Ustaw tą zmienną tak aby łazik jechał prosto.

# Notatka: Jeśli łazik będzie cały czas kręcił kołami mimo, że program nie jest uruchomiony to zrestartuj kontroler silnika.
# Notatka 2: Przy pierwszym uruchomieniu po włączeniu autka autko najprawdopodobniej nie będzie jechać bo kontroler będzie
# się wybudzał z uśpienia. Wtedy po prostu uruchom program jeszcze raz i łazik powinien jechać.

# Jazda
# drive_controller.throttle = 1.0 # MAX do przodu
# drive_controller.throttle = -1.0 # MAX do tyłu

# Skręcanie
# Aby skręcić w lewo ustaw wartość sterowania na wartość ujemną.
# Aby skręcić w prawo ustaw wartość sterowania na wartość dodatnią.
# Przykład który skręca w lewo.
# drive_controller.steering = -1.0 # MAX w lewo
# drive_controller.steering = 1.0 # MAX w prawo

# Opóźnienie
# sleep(1.0) # Czekaj 1 sekundę

def main():
    # Kod do jazdy.

if __name__ == "__main__":
    # Jeśli wystąpi błąd to go wyświetl i zatrzymaj silniki.
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
