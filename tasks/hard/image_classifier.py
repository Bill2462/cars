from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car.dnn import ImageClassifier, load_classes
import cv2

def resize_and_crop(img):
    img = cv2.resize(img, (398, 224))
    img = img[0:224, 87:311]
    return img

def preprocess_image(img):
    mean = np.array([0.485, 0.456, 0.406]).astype(np.float32)
    stddev = np.array([0.229, 0.224, 0.225]).astype(np.float32)
    # Zaimplementuj kod do normalizacji obrazu.
    
    return np.moveaxis(data, 2, 0).astype(np.float16) # Switch from HWC to to CHW order

def main():
    telemetry = TelemetrySender()
    cam = CSICamera()
    
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
