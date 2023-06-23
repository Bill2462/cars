# Zadanie 1

Zadanie ma na celu zapoznanie się z jazdą i ustalenie offsetu kół.

Szablon zadania znajduje się w pliku `driving.py`.

## Wersja łatwa

Szablon wersji łatwiejszej zaweiera gotowy kod który jedzie do przodu i do tyłu.
Najpierw przetetuj czy kod działa. Potem poeksperymentuj z parametrem steering i throttle i zobacz jak łazik skręca w lewo i prawo.

Poeksperymentuj z dodaniem kilku dodatkowych ruchów np. spraw aby łazik jechał prosto, skręcał w lewo, jechał kawałek prosto a potem skręcał w prawo.

UWAGA: Bezpieczne wartości dla throttle to wartości z przedziału od -0.3 do 0.3. Wartości poza tym sprawiają, że łazik jedzie bardzo szybko.

## Wersja trudniejsza

Szablon wersji trudniejszej zawiera tylko podstawowy kod.

Napisz kod który sprawi, że łazik będzie jechał do przodu i do tyłu. Potem poeksperymentuj z parametrem steering i throttle i zobacz jak łazik skręca w lewo i prawo.

UWAGA: Bezpieczne wartości dla throttle to wartości z przedziału od -0.3 do 0.3. Wartości poza tym sprawiają, że łazik jedzie bardzo szybko.

# Zadanie 2

Kontynuuj edycję kodu w pliku `driving.py` z zadania 1. Spraw aby łazik jechał tylko kawałe do przodu i się zatrzymywał.
Powoli zmieniaj wartość parametru steering_offset aż łazik zacznie jechać prosto przy wartości steering równej 0.

# Zadanie 3

Kontynuuj edycję kodu w pliku `driving.py` z zadania 2. Zaprogramuj prostą trasę dla łazika. Np jedź prosto, skręć w lewo, jedź prosto....

# Zadanie 4

Zadanie ma na celu implementację sterowania łazikiem za pomocą klawiatury albo pada.

Szablon zadania znajduje się w pliku `control_from_pad.py` w przypadku gamepada i `control_from_keyboard.py` w przypadku klawiatury.

W wersji łatwej szablon zawiera więcej przykładowego kodu niż w wersji trudnej.

Dodatkowe informacje znajdują się w komentarzach w kodzie.

# Zadanie 5

Zadanie ma na celu implementacje prostej pętli kontrolnej która będzie sprawiała, że łazik będzie jechał do markera wizyjnego.

Szablon zadania znajduje się w pliku `drive_to_aruco.py`.

W wersji łatwej szablon zawiera gotowy kod kontrolera proporcjonalnego. Należy tylko dobrać wzmocnienie proporcjonalnego kontrolera.

W wersji trudniejszej należy napisać formułę obliczającą błąd na podstawie pozycji markera i zaimplementować formułę kontrolera proporcjonalnego.

Na komputurze uruchom monitor kamery aby mieć podgląd na to czy marker jest poprawnie wykrywany.

WAŻNE:

Na autku włącz tryb MAXN (maksymalna moc obliczeniowa procesora). W konsoli ssh wpisz

```
jtop
```

Przejdź do zakładki `ctrl` i kliknij na `maxn` po czym wciśnij q aby wyjść.


Dla chętnych: Zaimplementuj pełny regulator PI albo PID.


## Formuła obliczenia błędu na podstawie pozycji markera

$$ 
e(x) = \frac{2x}{width} - 1
$$

 - $e(x)$ - Błąd
 - $x$ - Komponent X pozycji markera na obrazie.
 - $width$ - Szerokość obrazu

## Kontroler proporcjonalny

Wzór na sygnał sterowania:

$$ 
y(t) = kp \cdot e(t)
$$

 - $y(e)$ - Sygnał sterowania do kierownicy,
 - $e$ - Błąd
 - $kp$ - Wzmocnienie proporcjonalne

Wartość $y(e)$ należy ustawić na steering. Wewnętrznie zostanie ona ograniczona do zakresu $[-1, 1]$ więc nie trzeba tego umieszczać w kodzie.

## Kontroler całkujący

Wzór na sygnał sterowania:

$$ 
I_r = I_{t-1} + K_c E \frac{T_S}{T_i}
$$

 - $I_r$ - Stan wyjścia kontrolera
 - $I_{t-1}$ - Poprzedni stan wyjścia kontrolera
 - $T_s$ - Czas próvkowania.
 - $K_c$ - Wzmocnienie całkujące
 - $E$ - Błąd
 - $T_i$ - Czas całkowania (im większy tym wolniej kontroler będzie reagował na zmiany).

Wartość $y(e)$ należy ustawić na steering. Wewnętrznie zostanie ona ograniczona do zakresu $[-1, 1]$ więc nie trzeba tego umieszczać w kodzie.

## Kalibracja pętli kontroli

Należy postawić łazik na ziemi i umieścić marker na wprost nieco po lewej lub po prawej stronie od osi centralnej łazika. Następnie należy włączyć program kontrolny. Należy zacząć od małych wartości $kp$ i zwiększać je aż do momentu gdy łazik zacznie  jechać do celu.

## Zadanie 6

Kontynuuj edycję kodu z zadania 5. Zaprogramuj łazik tak aby jechał od markera do markera.

Aby to zrobić zaprogramuj najpierw jazdę do jednego markera. Potem jak marker stanie się dostatecznie szeroki. Łazik powinien skręcić w prawo albo w lewo aż w polu widzenia znajdzie się następny marker. Po czym powinien pojechać do następnego
markera i tak dalej aż do ostatniego markera.
