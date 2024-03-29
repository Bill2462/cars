from car.camera import CSICamera, NonBlockingCamera
from car.telemetry import TelemetrySender
from car.marker_detector import ArucoDetector
from car.drive import Car
import cv2

drive_controller = Car()
STEERING_OFFSET = 0.0 # Ustaw tutaj wartość offsetu sterowania ustaloną w zadaniu z podstawami sterowania.

MARKER_ID = 0 # Identyfikator markeru który będziemy śledzić. Jest na kartce z markerem.

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
    cam = CSICamera() # Jeśli jest problem z opóźnieniem możesz spróbować użyć NonBlockingCamera zmiast CSICamera. Zakomentuj linijkę powyżej

    while 1:
        frame = cam.read()

        # Detekcja markerów. Zwrca X i Y środka markeru.
        result, width = aruco_detector.detect_marker(frame, MARKER_ID)

        # Narysuj marker na obrazie.
        frame = draw_marker(frame, result)

        # Konwersja z BGR do RGB aby wyświetlanie obrazu na komputerze działało poprawnie.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        telemetry.log_image("img", frame) # Wyślij obraz do komputera.

        # Jeśli nie znaleziono markera to zatrzymaj łazik.
        if result is None:
            drive_controller.throttle = 0
            continue # Wróć do początku pętli.
        
        # Jedź do przodu z małą prędkością.
        drive_controller.throttle = 0.23
        
        frame_width = frame.shape[1]
        marker_center_x = result[0]

        # Implementacja regulatora proporcjonalnego.
        error = (marker_center_x / frame_width)*2 - 1
        turn_setting = KP * error

        # Ustaw sterowania
        drive_controller.steering = turn_setting + STEERING_OFFSET
        
        # Wyświetl błąd i ustawienie sterowania.
        print(error, turn_setting)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        drive_controller.stop()
