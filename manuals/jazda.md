## Przed rozpoczęciem

Zaloguj się do samochodzika przez konsolę ssh w terminalu.
```
ssh jetson@ADRES_IP
```

Przejdź do folderu `tasks/hard` lub `tasks/simple`.

`tasks/simple` zawiera szkielety programów które mają więcej uzupełnionych komponentów.

```
# trudne zadania
cd tasks/hard

# łatwe zadania
cd tasks/simple
```

Wpisz hasło `jetson` i naciśnij enter.

W vscode studio otwórz folder `/home/jetson/tasks/POZIOM TRUDNOŚCI` za pomocą remote explorer.

## Zadania

Napisz program w pythonie który sprawi że samochód pojedzie do przodu, skręci, i cofnie się do tyłu.

Napisz program który umożliwi jazdę z korektą na niedoskonałości w kontroli kierunku jazdy.

Napisz program w pythonie który umożliwi sterowaniem łazikiem za pomocą gamepada.

## Sterowanie samochodem

Otwórz plik `simple_drive.py`. Plik zawiera już napisany szkielet programu który pozwala na jazdę samochodzikiem.

Aby sterować samochdem należy ustawić parametry: `car.steering` i `car.throttle`.

Ustawienie silnika napędu i ustawienie pozycji serwa to liczby w zakresie od -1 do 1. W przypadku napędu -1 oznacza jazdę do tyłu z pełną prędkością a 1 do przodu z pełną prędkością.
W przypadku serwa -1 to pełne wychylenie w lewo a 1 to pełne wychylenie w prawo.

Przykład:

```
car.steering = 0.5
car.throttle = 0.2
```

UWAGA: Nie ustawiać throttle na wartości większe niż 0.3 albo mniejsze niż -0.3 bo samochód pojedzie bardzo szybko i najprawdopodobniej nie będzie już w jednym kawałku.

Użyj `sleep(ilość sekund)` aby dodaj opóźnienie.

## Formuła korekty sterowania

$$ y = a\cdot x + b $$

 - $ y $ - Sygnał sterujący serwomechanizmem
 - $ x $ - Sygnał sterujący z programu
 - $ a $ - Zysk
 - $ b $ - Offset

## Korekta sterowania

Zmodyfikuj skrypt `simple_drive.py`.

Napisz funkcję w pythonie która zaimplementuje formułę korekty sterowania.

Przykładowa funkcja pythona:

```
def x(a, b=12):
    return a + b
```     

W tym przykładzie `a` to wymagany parametr a `b` to opcjonalny parametr. Funkcja zwraca sumę parametrów.

Zacznij od `offset = 0` i `gain = 1`.

Najpierw ustaw offset tak aby samochód jechał prosto. Testuj jazdę na krótkich przejazdach zmieniając sukcesywnie wartość offsetu aż samoch»d pojedzie prosto przy `x=0`. Zmiana parametru `gain` nie jest potrzebna w tym zadaniu.

Program jest uruchamiany komendą:

```
python3 simple_drive.py
```

## Odczyt danych z gamepada

Otwórz plik `gamepad_drive.py`.

Skrypt zawiera już kod do odczytu stanu gamepada.

Zmienne x i y mogą mieć wartość -1, 0 albo 1.

W przypadku zmiennej x 1 oznacza, że lewy przycisk jest wciśnięty, -1 oznacza, że prawy przycisk jest wciśnięty a 0 oznacza, że ani prawy ani lewy przycisk nie są wciśnięte.

W przypadku zmiennej y 1 oznacza, że górny przycisk jest wciśnięty, -1 oznacza, że dolny przycisk jest wciśnięty a 0 oznacza, że ani górny ani dolny przycisk nie są wciśnięte.

Zmodyfikuj skrypt tak aby samochód jechał do przodu gdy górny przycisk jest wciśnięty, do tyłu gdy dolny przycisk jest wciśnięty, w lewo gdy lewy przycisk jest wciśnięty i w prawo gdy prawy przycisk jest wciśnięty.

Do skryptu skopiuj funkcję do korektą sterowania z poprzedniego zadania.

Dobierz parametr `gain` tak aby łazikiem się wygodnie skręcało za pomocą pada.

Notatka: odczyt stanu kontrolera gier wymaga uruchomienia skryptu jak root:

```
sudo python3 gamepad_drive.py
```

