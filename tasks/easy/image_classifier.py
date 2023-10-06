from car.camera import CSICamera, NonBlockingCamera
from car.telemetry import TelemetrySender
from car.image_classifier import ImageClassifier, preprocess_image, resize_and_crop, load_classes, softmax, get_top_k
import cv2


## Funkcje pomocnicze z któr
# Normalizacja i zamiana na format HWC.
# frame = preprocess_image(frame)

# Inferecjna sieci neuronowej.
# logits = classifier.inference(frame)

# Softamx
# probs = softmax(logits)

# Wybierz 10 najbardziej prawdopodobnych klas.
# topk = get_top_k(probs, 10)

# Wyczyść konsolę.
# print("\033c")

# Wyświetl klasę i prawdopodobieństwo dla każdej z 10 najbardziej prawdopodobnych klas.
# for i in topk:
#     print(class_labels[i], probs[i])

def main():
    telemetry = TelemetrySender()
    cam = CSICamera() # Jeśli jest problem z opóźnieniem możesz spróbować użyć NonBlockingCamera zmiast CSICamera. Zakomentuj linijkę powyżej

    
    # Załaduj model siecu neuronowego zoptymalizowany przez TensorRT.
    classifier = ImageClassifier('/home/jetson/tasks/efficient_net_b3.trt')

    # Załaduj etykiety klas.
    class_labels = load_classes('/home/jetson/tasks/imagenet_classes.txt')

    while True:
        frame = cam.read()
        # przeskaluj obraz do rozmiaru 224x224
        frame = resize_and_crop(frame)

        # Zamień kanały kolorów z BGR na RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        telemetry.log_image("img", frame)

        # Umieść tutaj kod który do inference sieci neuronowej.
        
if __name__ == '__main__':
    main()
