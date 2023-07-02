# Repozytorium kursu z jazdy autonomicznej

To repozytorium zawiera kod źródłowy, instrukcje i przykłady do platformy jetracer.

Struktura repozytorium:

- `envs` - Pliki do tworzenia środowiska conda.
- `examples` - Gotowe przykłady.
- `manuals` - Instrukcje do zadań
- `packages` - Kod do pakietu obsługi samochodu.
- `services` - Kod do serwisów.
- `setup` - Zasoby do instalacji wszystkich pakietów na system jetson-os.
- `tasks` - Szablony kodu do zadań.

## Szablony kodu do zadań

W katalogu `tasks` znajdują się szablony kodu do zadań. Są one zlokalizowane w katalogach o nazwach `easy` i `hard`.
Zadania są te same ale różnią ilością już napisanego kodu w szablonie. Zadania `easy` zawierają więcej kodu niż `hard`.
Zadania `easy` są przeznaczone dla osób które nie mają doświadczenia w programowaniu w pythonie.
Zadania `hard` są przeznaczone dla osób które mają doświadczenie w programowaniu w pythonie.

Zadania na dzień 1:
 - `driving.py` - Jazda i korekta sterowania.
 - `control_from_pad.py` - Sterowanie z gamepada.
 - `control_from_keyboard.py` - Sterowanie z klawiatury jeśli gamepad nie działa.
 - `drive_to_aruco.py` - Jazda do markera auroco.

Zadania na dzień 2:
 - `image_classifier.py` - Klasifikacja obrazów.
 - `drive_to_object.py` - Jazda do obiektu wykrytego przez YOLO.

## Pobieranie repozytorium i przygotowanie środowiska conda

Otwórz wiersz poleceń. Wykonaj:

```
git clone https://github.com/Bill2462/cars
```

Potem zainstaluj środowiska opisane w `env_windows.yaml` wykonując komendy:

```
cd cars/envs
conda env create -f env_windows.yaml
```

## Łączenie się z autkiem przez ssh

Otwórz command line prompt na windowsie i wpisz:

```
ssh jetson@ADRES_IP
```

Hasło to jetson. ADRES_IP to adres IP twojego autka np `192.168.5.108`. Jeśli komenda poprosi o potwierdzenie sygnatury to potwierdź ją.

Jeśli wyskoczy błąd o zmianie identyfikacji to otwórz w dowolnym edytorze tekstu plik którego ścieżka znajduje się w komunikacie i usuń
linijkę która zawiera adres IP samochodzika. Potem komenda powinna działać.

## Łączenie się z autkiem w vscode studio

Otwórz vscode studio. Wybierz Remote Expler z menu po lewej. Dodaj nowe połączenie (przycisk + przy zakładce ssh)

```
ssh jetson@ADRES_IP
```

Odświerz listę połączeń (klikając na strzałkę). Połącz się  ze swoim auktiem (klikając na strzłkę w prawo przy adresie IP twojego autka), wpisz hasło jestson
Jeżeli w lewym dolnym rogu widać SSH:ADRES_IP znaczy się jesteś połączony z autkiem.
Jeżel środowisko pyta o platformę wybierz Linux. Wpisuj hasło zawsze kiedy poprosi.
Wejdź do katalogu /home/jetson/tasks. Wybierz poziom trudnośći po przerzez wejście do odpowiedniego katalogu.

Teraz możesz skokpiować odpowiedni szablon zadania, które chcesz edytować i zacząć nad nim pracować.

## Uruchamianie zadań

Najpierw zaloguj się na autko przez ssh i przejdź do katalogu z zadaniem.
Następnie uruchom zadanie.

```
python3 NAZWA_ZADANIA.py
```
Aby zakończyć wykonywanie kodu wciśnij ctrl+c.

Zadanie dotyczące gamepada i klawiatury wymaga uruchomienia jako administrator (root). Komenda w przypadku tych zadań to

```
sudo python3 NAZWA_ZADANIA.py
```

Podaj hasło jestson i naciśnij enter.

## Aktywacja środowiska conda

Monitor kamery i przygotowanie modelu wymaga uruchomienia programu napisanego w pythonie3 wewnątrz środowiska conda które zawiera wszystkie potrzebne biblioteki.

Aby aktywować środowisko conda wyszukaja w menu start program `Anaconda Prompt (anaconda3)`. Uruchom go i wpisz:

```
conda activate car
```

## Uruchamianie monitora kamery 

Najpierw aktywuj środowisko conda. Następnie przejdź do katalogu `cars` w folderze students. Uruchom program monitora kamery.

```
python camera_monitor.py --ip ADRES_IP img
```

ADRES_IP to adres IP twojego autka.

Notatka: Program na autko który zwraca obraz z kamery musi być uruchomiony przed wykonaniem tego skryptu.



$$
y = g(x)
$$