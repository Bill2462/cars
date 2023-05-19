
## Zadania

Napisz skrypt w pythonie który pobierze obraz z kamery i zapisze go w pliku .png.

Pobierz plik z jetsona i wyświetl go na komputerze.

Napisz skrypt w pythonie który w pętli nieskończonej będzie wysyłał co 0.5 sekundy obraz z kamery do telemetrii tak aby można go było wyświetlić na komputerze.

## Co trzeba zrobić po kolei?

 - Otwórz edytor vscode studio na jetsonie (plugin ssh-remote)
 - Stwórz nowy folder w /home/jetson.
 - Stwórz nowy plik tekstowy z rozszerzeniem.py w którym napiszesz program.
 - Napisz program w tym pliku.
 - Otwórz konsolę windowsa i otwórz terminal ssh za pomocą komendy ssh.
 - W konsoli ssh przejdź do folderu gdzie utworzyłeś jest twój program (cd) i go uruchom.
 - Otwórz drugą konsolę windowsa i pobierz zdjęcie za pomocą sftp.
 - Napisz program do wysyłania zdjęć z kamery.
 - Na komputerze otwórz konsolę anacondy
 - Sklonuj repozytorium projektu z githuba.
 - Przejdź do folderu `jetracer-tools`
 - Aktywuj środowisko `cars` za pomocą condy.
 - Na jetsonie uruchom program do wysyłania zdjęć który napisałeś.
 - Na hoście w konsoli anacondy uruchom skrypt do wyświetlania obrazu.

## Komponenty skryptu

Import klasy kamery i telemetrii z pakietu car:

```
from car.camera import CSICamera
from car.telemetry import TelemetrySender
```

Import pakietu opencv (przetwarzanie obrazu) i time (czas)

```
import cv2
import time
```

Opóźnienie:

```
time.sleep(ilość sekund jako float)
```

Pętla nieskończona (python nie używa {} jak java czy c++ tylko używa wcięć do oznaczania bloków kodu. ):

```
while 1:
    print("Hello world")
```

Tworzenie obiektu kamery:

```
obiekt_kamery = CSICamera()
```

Tworzenie obieku telemetrii:

```
obiekt_telemetrii = TelemetrySender()
```

Odczyt klatki obrazu za pomocą kamery:

```
klatka = obiekt_kamery.read()
```

Zapis obrazu na dysku za pomocą opencv.

```
cv2.imwrite(ściężka do pliku jako string, klatka)
```

Wysyłanie klatki za pomocą obiektu telemetrii:

```
obiekt_telemetrii = obiekt_telemetrii.log_image(nazwa kanału jako string, klatka)
```

## Wyświetlanie obrazu na komputerze

```
python camera_monitor.py --ip adres_ip nazwa kanału jako string
```

## Komendy w terminalu

Na linuxie:

Zmiana folderu na linuxie:

```
cd nowa_ścieżka

cd app/ # do folderu (w tym wypadku app)
cd ../ # do ścieżki powyżej
cd ~/ # do folderu domowego użytkownika
```

Kopiowanie plików

```
cp ścieżka_do_pliku_źrodłowego ścieżka_do_pliku_docelowego
cp main.py folder/main.py
```

Wykonywanie skryptu w pythonie na linuxie:

```
python3 ścieżka do pliku z programem
python3 app.py # wykona program app.pys
```

Na host:

Aktywowanie środowiska condy w którym będziemy pracować.

```
conda activate cars
```

Wejście do folderu projektu

```
cd ścieżka_do_projektu
```

Pobranie projektu z githuba.

```
git clone https://github.com/Bill2462/jetracer-tools
```

Uruchomienie skryptu w pythonie:

```
python ścieżka do pliku z programem
```

Otworzenie konsoli zdalnej ssh

```
ssh użytkownik@adres_servera
ssh jetson@192.169.0.101
```

Otworzenie konsoli do przesyłania plików przez ssh.

```
sftp użytkownik@adres_servera
sftp jetson@192.169.0.101
```

Wewnątrz konsoli sftp takie są komendy podstawowe komendy:

```
# zmiana folderu zdalnego
cd nowa ścieżka
cd app/modules

# Pobieranie

get filename.zip local_filename.zip # plik
get -r folder # folder

# Wysyłanie

put filename.zip
get -r folder # folde

bye # wyjście z konsoli
```
