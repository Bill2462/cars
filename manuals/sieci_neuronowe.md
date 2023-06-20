## Przed rozpoczęciem

Zaloguj się do samochodzika przez konsolę ssh w terminalu.
    
```
ssh jetson@ADRES_IP
```

Wpisz hasło `jetson` i naciśnij enter.

W vscode studio otwórz folder `/home/jetson/tasks` za pomocą remote explorer.

Otwórz dwa okna terminala w folderze jetracer-tools. I w obu aktywuj środowisko anaconda o nazwie `car`.

Na windowsie okno terminala anaconda otwiera się przez wybieżenie `Anaconda Prompt (anaconda3)` z menu start.

Środowisko car należy aktywować w obu oknach komendą:

```
conda activate car
```

W jednym oknie terminala uruchom serwer jupyter notebook komendą:

```
jupyter notebook
```

Drugie okno zachowaj na razie bezczynne.

## Zadania

Napisz program który będzie klasyfikował obrazki z kamery za pomocą pretrenowanej sieci neuronowej mobilenet.


## Krok 1 - Pobranie pretrenowanego modelu i eksport do ONNX

Utwórz nowy dokument jupyter notebook.

W pierwszej komórce wpisz:

```
import torchvision.models as models
import torch
import torch.onnx
```

Pobierz model mobilenetb2 i ustaw go w trybie ewaluacji komendą:

```
model = models.mobilenet_b2(pretrained=True).eval()
```

Stwórz przykładowy tensor o wymiarach 3x224x224 i zapisz go do zmiennej `dummy_input`:

```
dummy_input = torch.randn(1, 3, 224, 224)
```

Eksportuj model do formatu ONNX:

```
torch.onnx.export(model, dummy_input, "model.onnx")
```

Skopiuj plik `model.onnx` do folderu `tasks` na samochodziku za pomocą vscode.

## Krok 2 - Optymalizacja modelu za pomocą TensorRT

W terminalu ssh przejdź do folderu `tasks` i uruchom komendę:

```
/usr/src/tensorrt/bin/trtexec --onnx=model.onnx --saveEngine=model.trt --explicitBatch  --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16

```

Po kilku minutach powinien pojawić się plik `model.trt`.


## Krok 3 - Program do inferencji

W vscode otwórz plik `tasks/model_inference.py`.

### Ładowanie modelu do pamięci i alokacja pamięci na dane wejściowe i wyjściowe

Najpierw stwórz logger i runtime.

```
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
runtime = trt.Runtime(TRT_LOGGER)
```

Potem załaduj model i zdeserializuj go do pamięci GPU.

``` 
with open("model.trt", "rb") as f:
    engine = runtime.deserialize_cuda_engine(f.read())
```

Teraz należy zaalokować pamięć CPU i GPU na dane wejściowe i wyjściowe.

Aby to zrobić należy najpierw przygotować listy które będą zawierały obiekty.

```
host_inputs  = [] # Wejścia na CPU
cuda_inputs  = [] # Wejścia na GPU
host_outputs = [] # Wyjścia na CPU
cuda_outputs = [] # Wyjścia na GPU
bindings = [] # Lista związująca wejścia i wyjścia z obiektami
```
Teraz musimy stworzyć pętlę która będzie iterowała przez każde związania:

```
for binding in engine:
    # Kod do alokacji pamięci
```

Dla każdego zwiazania musimy obliczyć rozmiar alokowanej pamięci:

```
size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
```

Następnie musimy zaalokować pamięć w obszarze CPU i GPU:

```
host_mem = cuda.pagelocked_empty(shape=[size], dtype=np.float16) # CPU
cuda_mem = cuda.mem_alloc(host_mem.nbytes) # GPU
```

Teraz musimy dodać obiekty do list:

```
bindings.append(int(cuda_mem))
if engine.binding_is_input(binding):
    host_inputs.append(host_mem)
    cuda_inputs.append(cuda_mem)
else:
    host_outputs.append(host_mem)
    cuda_outputs.append(cuda_mem)
```

Ostatnim krokiem do przygotowania modelu do wykonania jest stworzenie konetekstu wykonawczego i strumienia CUDA:

```
context = engine.create_execution_context()
stream = cuda.Stream()

```

Notatka: Powyższy kod powinien zostać wykonany tylko raz na początku programu.

### Przygotowanie obrazu

Najpierw musimy zmniejszyć rozmiar obrazu do 398x224.
Zachowa to proporcje obrazu i pozwoli na uniknięcie zniekształceń.

Następnie należy przyciąć obraz do wymiarów 224x224.

Funkcja do zmniejszania obrazu:

```
nowy_obraz = cv2.resize(obraz, rozmiar)
```

Przycinanie można wykonać za pomocą zakresów w pythonie:

```
nowy_obraz = obraz[index_start_rząd:index_stop_rząd, index_start_kolumna:index_stop_rząd]
```

Powyższy kod wycina obraz od `index_start_rząd` do `index_stop_rząd` wiersza i od `index_start_kolumna` do `index_stop_kolumna` kolumny.

Następnie należy zmienić kolejność kanałów z BGR na RGB.

```
nowy_obraz = cv2.cvtColor(obraz, cv2.COLOR_BGR2RGB)
```


Następnie należy znormalizować obraz.

W tym celu należy go najpierw podzielić przez 255 aby uzyskać wartości z zakresu 0-1.

```
nowy_obraz = obraz.astype(np.float32) / 255.0
```

Następnie należy od każdego pixela odjąć średnią kanału i podzielić przez odchylenie standardowe kanału. 
Wartości dla każdego kanału są predefiniowane dla modelu mobilenetb2. Zostały one obliczne na podstawie zbioru treningowego ImageNet.

```
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
stddev = np.array([0.229, 0.224, 0.225], dtype=np.float32)
nowy_obraz = (obraz - mean) / stddev
```

Następnie należy zamienić kolejność kanałów z HWC na CHW.

```
nowy_obraz = np.moveaxis(obraz, 2, 0)
```

Na końcu zamieniamy typ danych na float16 aby pasował do modelu.

```
nowy_obraz = obraz.astype(np.float16)
```

### Inferencja modelu

Teraz pora na kod który będzie wykonywał inferencję modelu.

Najpierw należy skopiować dane wejściowe do pamięci CPU zablokowanej stronicowo za pomocą funkcji `np.copyto()`:

```
np.copyto(host_inputs[0], obraz.ravel())
```

Ravel jest funkcją która zamienia tablicę wielowymiarową na jednowymiarową.

Następnie kopiujemy obraz do pamięci GPU:
```
cuda.memcpy_htod_async(cuda_inputs[0], host_inputs[0], stream)
```

Następnie wykonujemy inferencję modelu:

```
context.execute_async(bindings=bindings, stream_handle=stream.handle)
```

Potem kopiujemy wyniki z pamięci GPU do pamięci CPU:

```
cuda.memcpy_dtoh_async(host_outputs[0], cuda_outputs[0], stream)
```

Na końcu czekamy na zakończenie operacji na strumieniu:

```
stream.synchronize()
```

Operacje na GPU wykonywane są asynchronicznie. Dlatego musimy czekać na zakończenie operacji na strumieniu aby mieć pewność że wyniki są gotowe.

Na końcu musimy przekonwertować wyniki do kształtu który oryginale zwraca model:

```
wynik = host_outputs[0].reshape(np.concatenate(([1],engine.get_binding_shape(1))))
```

### Obróbka i wyświetlenie wyników modelu

Najpierw musimy przekonwertować wynik do postaci czytelnej dla człowieka:

Aby to zrobić najpierw musimy załadować nazwy klas odpowiadjące kolejnym wyjścią modelu:

```
with open("imagenet_classes.txt", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
```

Klasy powinny być załadowane poza pętlą. W przeciwnym razie będą załadowane przy każdej iteracji pętli co jest niepotrzebne.

Następnie musimy zaaplikować funkcję softmax do wyników modelu za pomocą numpy:

```
wynik = np.squeeze(wynik)
wynik = np.exp(wynik) / np.sum(np.exp(wynik))
```

Squeeze jest funkcją która usuwa wymiary o rozmiarze 1. Możemy sobie na to tutaj pozwolić ponieważ przepuszczamy jedną próbkę na raz.
Jeśli mielibyśmy doczynienia z większą ilością próbek to musielibyśmy ustawić opdowiednio parametr `axis` aby operacje
były wykonywane po odpowiednich wymiarach.

Wreszcie musimy wybrać 5 najbardziej prawdopodobnych klas:

```
top_k = wynik.argsort()[-5:][::-1]
```

I wyświetlić odpowiadające im nazwy:

```
# Wyczyść ekran terminala
os.system('clear')

for i in top_k:
    print(classes[i], wynik[i])
```

## Krok 4 - Uruchomienie programu


W terminalu ssh przejdź do folderu `tasks` i uruchom komendę:

```
python3 model_inference.py
```

Na komputerze w terminalu otwórz monitor kamery za pomocą komendy:

``` 
python camera_monitor.py --ip ADRES_IP img
```
