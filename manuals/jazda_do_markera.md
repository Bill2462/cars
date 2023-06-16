## Przed rozpoczęciem

Zaloguj się do samochodzika przez konsolę ssh w terminalu i przejdź do folderu `tasks/hard` lub `tasks/simple`.

`tasks/simple` zawiera szkielety programów które mają więcej uzupełnionych komponentów.

```
ssh jetson@ADRES_IP

# trudne zadania
cd tasks/hard

# łatwe zadania
cd tasks/simple
```

Wpisz hasło `jetson` i naciśnij enter.

W osobnym terminalu otwórz terminal anaconda i aktywuj środowisko `car` za pomocą komendu `conda activate car`.
Po czym przejdź do folderu `student/jetracer-tools` za pomocą komendy `cd`.

Na windowsie terminal anaconda znajduje się w menu start i nazywa się anaconda prompt.

W vscode studio otwórz folder `/home/jetson/tasks/POZIOM TRUDNOŚCI` za pomocą remote explorer.

## Zadania

Napisz program w pythonie który sprawi że samochód pojedzie w kierunku markera.

## Komponenty implementacji sterowania

Otwórz plik `driving_to_aruco.py`. Plik zawiera już napisany szkielet programu który pozwala na jazdę samochodzikiem.


Kiedy marker nie jest wykrywany result to jest `None`. Wtedy należy ustawić napęd na 0.

Instrukcja warunkowa if do sprawdzenia tego warunku:
```
if result is None:
    USTAW NAPĘD NA 0
    continue
```

`continue` powoduje przejście do następnej iteracji pętli bez wykonania reszty instrukcji. 

Aby uzyskać pozycję markera (w pixelach) na obrazie należy użyć:

```
x_marker = result[0]
```

Aby uzyskać szerokość obrazu (w pixelach) należy użyć:

```
image_width = frame.shape[1]
```

Następnie należy zaimplementować formułę obliczenia błędu na podstawie pozycji markera.


## Formuła obliczenia błędu na podstawie pozycji markera

$$ e(x) = \frac{2x}{width} - 1$$

 - $ e(x) $ - Błąd
 - $ x $ - Komponent X pozycji markera na obrazie.
 - $ width $ - Szerokość obrazu

## Pętla kontroli 

W tym wypadku nie potrzebujemy kontrolera całkowego ani różniczkowego. Wystarczy nam tylko proporcjonalny.

Wzór na sterowanie:
$$ y(e) = kp \cdot e$$

 - $ y(e) $ - Sygnał sterowania do kierownicy,
 - $ e $ - Błąd
 - $ kp $ - Wzmocnienie proporcjonalne

Wartość $y(e)$ należy ustawić na steering. Wewnętrznie zostanie ona ograniczona do zakresu $[-1, 1]$ więc nie trzeba tego umieszczać w kodzie.

## Kalibracja pętli kontroli

Należy postawić łazik na ziemi i umieścić marker na wprost nieco po lewej lub po prawej stronie od osi centralnej łazika. Następnie należy włączyć program kontrolny. Należy zacząć od małych wartości $kp$ i zwiększać je aż do momentu gdy łazik zacznie  jechać do celu.

