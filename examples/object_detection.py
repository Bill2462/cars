from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car import darknet
from car.drive import Car

import cv2
import time

def correct_steering(x, offset=0.1464, gain=1.0):
    return x*gain + offset

drive_controller = Car()
Kp = 0.8

def resize_and_crop(img):
    img = cv2.resize(img, (740, 416))
    img = img[:, 152:568]
    return img

def main():
    telemetry = TelemetrySender()
    cam = CSICamera()

    network, class_names, class_colors = darknet.load_network(
            "../../yolo_bin/yolov4-tiny.cfg",
            "../../yolo_bin/coco.data",
            "../../yolo_bin/yolov4-tiny.weights",
            batch_size=1
        )

    darknet_image = darknet.make_image(416, 416, 3)
    next_move = 0
    MOVE_LEN = 0.5
    MOVE_INTERVAL = 1.5
    while True:
        frame = cam.read()
        frame = resize_and_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        darknet.copy_image_from_bytes(darknet_image, frame.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.1)

        frame = darknet.draw_boxes(detections, frame, class_colors)

        telemetry.log_image("img", frame)
        
        found = False
        for object in detections:
            if object[0] == "bottle":
                found = True
                bottle_x = object[2][0]
        
        if not found:
            drive_controller.throttle = 0
            continue

        if next_move < time.time():
            drive_controller.throttle = 0.18
            time.sleep(MOVE_LEN)
            drive_controller.throttle = 0
            next_move = time.time() + MOVE_INTERVAL
       
        error = (bottle_x / frame.shape[1])*2 - 1
        turn_setting = Kp * error
        drive_controller.steering = correct_steering(turn_setting)
        
        print(error, turn_setting)
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
