## Przed rozpoczęciem

Zaloguj się do samochodzika przez konsolę ssh w terminalu.
    
```
ssh jetson@ADRES_IP
```

Wpisz hasło `jetson` i naciśnij enter.

W vscode studio otwórz folder `/home/jetson/tasks` za pomocą remote explorer.

## Zadania

Napisz program w pythonie który sprawi że samochód pojedzie do przodu, skręci, i cofnie się do tyłu.

Napisz program który umożliwi jazdę z korektą na niedoskonałości w kontroli kierunku jazdy.

Napisz program w pythonie który umożliwi sterowaniem łazikiem za pomocą gamepada.

## Sterowanie samochodem

Otwórz plik z `simple_drive.py`. Plik zawiera już napisany szkielet programu który pozwala na jazdę samochodzikiem.

Aby sterować samochdem należy ustawić parametry: `car.steering` i `car.throttle`.

Ustawienie silnika napędu i ustawienie pozycji serwa to liczby w zakresie od -1 do 1. W przypadku napędu -1 oznacza jazdę do tyłu z pełną prędkością a 1 do przodu z pełną prędkością.
W przypadku serwa -1 to pełne wychylenie w lewo a 1 to pełne wychylenie w prawo.

Przykład:

```
car.steering = 0.5
car.throttle = 0.2
```

UWAGA: Nie ustawiać throttle na wartości większe niż 0.3 albo mniejsze niż -0.3 bo samochód pojedzie bardzo szybko i najprawdopodobniej nie będzie już w jednym kawałku.

## Korekta sterowania

Zmodyfikuj skrypt `simple_drive.py`.

Napisz funkcję w pythonie która zaimplementuje tą formułę: 

$$ y = gain\cdot x + offset$$

Przykładowa funkcja pythona:

```
def x(a, b=12):
    return a + b
```     

W tym przykładzie `a` to wymagany parametr a `b` to opcjonalny parametr. Funkcja zwraca sumę parametrów.

Wykonywanie różnego kodu w zależności od znaku liczby wygląda tak.

```
if x <= 0:
    print("x jest mniejsze lub równe 0")
else:
    print("x jest większe od 0")
```

Notatka: Inaczej niż w C++ C, i Java parametry ustawione wewnątrz bloków kodu są widoczne na zewnątrz. Przykład:

```
if x <= 0:
    y = 1
else:
    y = 2

print(y) # To działa!
```

Przypisz wartość z tej funkcji do `car.steering`.

Przetestuj różne wartości gain i offset tak aby samochód jechał prosto kiedy wejście kontrolne jest równe 0 i skręcał równo w lewo i w prawo kiedy wejście kontrolne jest równe -1 i 1.

Gain powinien być ustawiany osobno dla lewego i prawego kierunku jazdy.

Zacznij od `offset = 0` i `gain = 1`.

Program jest uruchamiany komendą:

```
python3 simple_drive.py
```

## Odczyt danych z gamepada

Otwórz plik `gamepad_drive.py`.

Skopiuj funkcję korekty i z poprzedniego zadania. Spraw aby samochód był kontrolowany za pomocą dpad z gamepada.

Odczyt stanu dpad z kontrolera:

```
x = float(gamepad.buttons.ABS_HAT0X.value)
y = float(gamepad.buttons.ABS_HAT0Y.value)
```

Zmienne x i y mogą mieć wartość -1, 0 albo 1.

W przypadku zmiennej x 1 oznacza, że lewy przycisk jest wciśnięty, -1 oznacza, że prawy przycisk jest wciśnięty a 0 oznacza, że ani prawy ani lewy przycisk nie są wciśnięte.

W przypadku zmiennej y 1 oznacza, że górny przycisk jest wciśnięty, -1 oznacza, że dolny przycisk jest wciśnięty a 0 oznacza, że ani górny ani dolny przycisk nie są wciśnięte.

Notatka: odczyt stanu kontrolera gier wymaga uruchomienia skryptu jak root:

```
sudo python3 gamepad_drive.py
```

