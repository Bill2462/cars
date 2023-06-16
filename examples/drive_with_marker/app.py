from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car.marker_detector import ArucoDetector
from car.drive import Car
import cv2

drive_controller = Car()

Kp = 0.5

def draw_marker(img, marker_center):
    # Write vertical line at the middle of the image
    cv2.line(img, (img.shape[1] // 2, 0), (img.shape[1] // 2, img.shape[0]), (0, 255, 0), 5)

    if marker_center is not None:
        cv2.circle(img, (marker_center[0], marker_center[1]), 30, (0, 255, 0), -1)
    return img

def main():
    telemetry = TelemetrySender()
    aruco_detector = ArucoDetector()
    cam = CSICamera()

    while 1:
        frame = cam.read()

        result = aruco_detector.detect_marker(frame)
        frame = draw_marker(frame, result)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        telemetry.log_image("img", frame)

        if result is None:
            drive_controller.throttle = 0
            continue
        
        drive_controller.throttle = 0.2
        
        error = (result[0] / frame.shape[1])*2 - 1
        turn_setting = Kp * error
        turn_setting = max(-1, min(turn_setting, 1))
        drive_controller.steering = turn_setting
        print(error, turn_setting)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()

