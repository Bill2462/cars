## Zadania

Napisz program w pythonie który sprawi że samochód pojedzie do przodu, skręci, i cofnie się do tyłu.

Napisz program w pythonie który umożliwi sterowaniem łazikiem za pomocą gamepada.

## Komponenty skryptu

Import klasy sterownika platformy jezdnej z pakietu car i pakietu do obsługi kontrolera.

```
from car.drive import DriveController
from pygamepad.gamepads.default import Gamepad
```

Tworzenie obiektu sterownika platformy jezdnej i kontrolera:

```
drive_controller = DriveController(dummy=False)
```

"dummy" to parametr który włacza tryb "na sucho". W tym trybie program wyświetla ustawienia w terminalu ale nie włącza napędu. Domyślnie `dummy=True` więc napęd by nie działał.
Stąd aby włączyć napęd musimy ustawić ten parametr na `False` i stąd linijka `dummy=False`.


Jazda:

```
drive_controller.drive(ustawienie silnika napędu, ustawienie pozycji serwa sterowania, czas jazdy w sekundach)
```

Ustawienie silnika napędu i ustawienie pozycji serwa to liczby w zakresie od -1 do 1. W przypadku napędu -1 oznacza jazdę do tyłu z pełną prędkością a 1 do przodu z pełną prędkością.
W przypadku serwa -1 to pełne wychylenie w lewo a 1 to pełne wychylenie w prawo.


Tworzenie obiektu gamepada i rozpoczęcie pobierania stanu kontrolera:

```
gamepad = Gamepad()
gamepad.listen()
```

Notatka: odczyt stanu kontrolera gier wymaga uruchomienia skryptu jak root:

```
sudo python3 program.py
```

Odczyt stanu dpad z kontrolera:

```
x = -gamepad.buttons.ABS_HAT0X.value
y = -gamepad.buttons.ABS_HAT0Y.value
```

Zmienne x i y mogą mieć wartość -1, 0 albo 1.

W przypadku zmiennej x 1 oznacza, że lewy przycisk jest wciśnięty, -1 oznacza, że prawy przycisk jest wciśnięty a 0 oznacza, że ani prawy ani lewy przycisk nie są wciśnięte.

W przypadku zmiennej y 1 oznacza, że górny przycisk jest wciśnięty, -1 oznacza, że dolny przycisk jest wciśnięty a 0 oznacza, że ani górny ani dolny przycisk nie są wciśnięte.

