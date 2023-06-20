from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car.dnn import ImageClassifier, preprocess_image, resize_and_crop, load_classes, softmax, get_top_k
import cv2

def main():
    telemetry = TelemetrySender()
    cam = CSICamera()

    classifier = ImageClassifier('../../efficient_net_b3.trt')
    class_labels = load_classes('imagenet_classes.txt')

    while True:
        frame = cam.read()
        frame = resize_and_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        telemetry.log_image("img", frame)

        frame = preprocess_image(frame)

        logits = classifier.inference(frame)
        probs = softmax(logits)
        topk = get_top_k(probs, 10)

        print("\033c")
        for i in topk:
            print(class_labels[i], probs[i])
        
if __name__ == '__main__':
    main()
