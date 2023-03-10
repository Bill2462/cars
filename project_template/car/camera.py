import cv2

class CSICamera:
    def __init__(self, capture_fps, capture_width, capture_height, width, height):
        try:
            self.capture_fps = capture_fps
            self.capture_width = capture_width
            self.capture_height = capture_height
            self.width = width
            self.height = height
            self.cap = cv2.VideoCapture(self._get_cmd_str(), cv2.CAP_GSTREAMER)

            re, _ = self.cap.read()

            if not re:
                raise RuntimeError("Could not read image from camera.")
        except:
            raise RuntimeError("Could not initialize camera.")
    
    def _get_cmd_str(self):
        cmd =  f"nvarguscamerasrc ! "
        cmd += f"video/x-raw(memory:NVMM), width={self.capture_width}, height={self.capture_height},"
        cmd += f" format=(string)NV12, framerate=(fraction){self.capture_fps}/1 ! nvvidconv ! video/x-raw,"
        cmd += f" width=(int){self.width}, height=(int){self.height}, format=(string)BGRx ! videoconvert ! appsink"
        return cmd

    def read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')
