# Zadanie 1

Cel to pobranie modelu z torchvision i napisanie programu do predykcji na podstawie obrazu z kamery.

Szablon zadania znajduje się w pliku `image_classifier.py`.

Należy najpierw pobrać model z torchvision. W tym celu należy użyć skryptu `download_model.py` który pobierze model i zapisze go do pliku onnx.
Skrypt należy uruchomić w terminalu anaconda w środowisku `car`.
Potem należy skopiować plik na autko przy użyciu vscode studio do folderu tasks.

W terminalu ssh przejdź do folderu `tasks` i uruchom komendę:

```
/usr/src/tensorrt/bin/trtexec --onnx=model.onnx --saveEngine=model.trt --explicitBatch  --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16

```

Zamień nazwy plików na prawidłowe.
Po kilku minutach powinien pojawić się plik z modelem.

Potem należy napisać kod do inferencji modelu. W prostej wersji należy użyć gotowych funkcji zaimplementowanych w pakiecie car.
W wersji trudnej należy napisać własną implementację softmax, normalizacji obrazu itd.

# Zadanie 2

Należy wytrenować model do rozpoznawania kwiatów. W tym celu należy edytować `train_cnn.ipynb` na platformie kaggle.

# Zadanie 3

Pobierz wytrenowany model i powtórz procedurę z zadania 1 aby uruchomić go na autku. 

# Zadanie 4

Napisz program który będzie jechał do dowolnego obiektu rozpoznawanego za pomocą sieci do wykrywnia obiektów YOLO.
