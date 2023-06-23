from car.camera import CSICamera
from car.telemetry import TelemetrySender
from car.marker_detector import ArucoDetector
from car.drive import Car
import cv2

drive_controller = Car()
drive_controller.steering_offset = 0.0 # Ustaw tutaj wartość offsetu sterowania ustaloną w zadaniu z podstawami sterowania.

MARKER_ID = 0 # Identyfikator markeru który będziemy śledzić.

KP = 0.0 # Zysk kontrolera proporcjonalnego.
# Ta zmienna kontroluje jak bardzo łazik będzie skręcał w stronę markeru.
# Im więcej tym szybciej koła się będę skręcały,

# WAZNE:
# Algorytm wykrywania markerów działa na CPU więc włącz wszystkie rdzenie procesora bo inaczej będzie bardzo wolno działał
# i łazik będzie skręcał z opóźnieniem.
# Aby to zrobić w terminalu ssh wpisz jtop i wciśnij enter.
# Wejdź w zakładkę ctrl klikając na nią myszką.
# Kliknij myszką na MAXN aby włączyć ten tryb.
# Potem wyjdź z programu jtop klikając ctrl + c albo q.

# Funkcja która rysuje marker na obrazie.
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

        # Detekcja markerów. Zwrca X i Y środka markeru.
        result, width = aruco_detector.detect_marker(frame, MARKER_ID)

        # Narysuj marker na obrazie.
        frame = draw_marker(frame, result)

        # Konwersja z BGR do RGB aby wyświetlanie obrazu na komputerze działało poprawnie.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        telemetry.log_image("img", frame) # Wyślij obraz do komputera.

        # Zaimplementuj formułę do liczenia błędu i kontroler pojemnościowy.
        # Jeśli result będzie None to powinniśmy wyłączyć silniki ustawiając throttle na 0.0.
        
        frame_width = frame.shape[1]
        marker_center_x = result[0]

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
