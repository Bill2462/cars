from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car.marker_detector import ArucoDetector
from car.drive import Car
import cv2

drive_controller = Car()

def draw_marker(img, marker_center):
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

        # Zmienić marker id na liczbę odpowiadającą stosowanemu markerowi.
        result = aruco_detector.detect_marker(frame, marker_id=0)
        frame = draw_marker(frame, result)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        telemetry.log_image("img", frame)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
