## Zadania

 - Użyj skryptu `examples/utils/capture_images.py` do zebrania zbioru zdjęć kalibracyjnych planszy (20-30 dobrych powinno wystarczyć)
 - Pobierz zdjęcia na PC używając sftp.
 - Na PC uruchom skrypt `do_camera_calibration.py` do obliczenia macierzy kamery i współczynników zniekształcenia.
 - Skopiuj plik .json zawierający parametry z kalibracji na jetsona.
 - Uruchom skrypt `examples/lens_correction/demo_fish_correction.py`.
 - Na PC uruchom dwa monitory obrazu na kanałach `img_uncorrected` (obraz bez korekty) i `img_corrected`. Porównaj obraz przed i po korektą.

## Skrypt do zbierania obrazów

```
python3 examples/utils/capture_images.py --single_shot ścieżka do folderu gdzie obrazy będą zapisane
```

W tym trybie `--single_shot` enter działa jak migawka. Podgląd jest dostępny na kanale `img`.

## Skrypt do demonstracji korekty soczewki

```
python3 examples/lens_correction/demo_fish_correction.py ściężka do pliku.json z parametrami.
```

W miarę dobrze działające parametry są dostępne w pliku `examples/lens_correction/calibration.json`.


