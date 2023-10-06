from car.camera import CSICamera, NonBlockingCamera
from car.telemetry import TelemetrySender
from car import darknet
from car.drive import Car

import cv2
import time

STEERING_OFFSET = 0.1464 # Ustaw offset z poprzednich zadań.

drive_controller = Car()
Kp = 0.8

def resize_and_crop(img):
    img = cv2.resize(img, (740, 416))
    img = img[:, 152:568]
    return img

def main():
    telemetry = TelemetrySender()
    cam = CSICamera() # Jeśli jest problem z opóźnieniem możesz spróbować użyć NonBlockingCamera zmiast CSICamera. Zakomentuj linijkę powyżej

    network, class_names, class_colors = darknet.load_network(
            "../../yolo_bin/yolov4-tiny.cfg",
            "../../yolo_bin/coco.data",
            "../../yolo_bin/yolov4-tiny.weights",
            batch_size=1
        )

    darknet_image = darknet.make_image(416, 416, 3)

    while True:
        frame = cam.read()
        frame = resize_and_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        darknet.copy_image_from_bytes(darknet_image, frame.tobytes())

        # Threshold ustawia minimalną pewność wykrycia obiektu.
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.1)

        frame = darknet.draw_boxes(detections, frame, class_colors)

        telemetry.log_image("img", frame)
        
        # Zaimplementuj wykrywanie obiektu i sterowanie samochodem tak aby jechał do dowolnego obiektu w sali.
        # Podpowiedź 1: Wykrywanie jest wolne. Zaimplementuj zatrzymanie się samochodu na 1.5 sekundy i ewaluację pozycji obiektu.
        # Podpowiedź 2: Zacznij od wyświetlenia surowych wyników w detetions. Zobacz jakie informacje są dostępne. Potem zaimplementuj wybór obiektu po nazwie.
        # Podpowiedź 3: Ramka jest zdefiniowana w taki sposób że koordynatę X jej środka można uzyskać za pomocą object[2][0].
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
