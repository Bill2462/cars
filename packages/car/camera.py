import cv2
import json
import vpi
import numpy as np

def load_camera_parameters(filepath):
    with open(filepath) as f:
        cfg = json.load(f)
        cam_matrix = np.array(cfg.get("camera_matrix"))
        dist_coeff = np.array(cfg.get("dist_coeff"))[0]
    
    return cam_matrix, dist_coeff

class CSICamera:
    def __init__(self, capture_fps=21, capture_width=1280, capture_height=720,
                 width=1280, height=720, camera_parameters_filepath=None):
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
        
        if camera_parameters_filepath:
            self.cam_matrix, self.dist_coeff = load_camera_parameters(camera_parameters_filepath)

            self.grid = vpi.WarpGrid((self.width, self.height))

            self.undist_map = vpi.WarpMap.fisheye_correction(self.grid,
                                                K=self.cam_matrix[0:2,:],
                                                X=np.eye(3,4),
                                                coeffs=self.dist_coeff,
                                                mapping=vpi.FisheyeMapping.EQUIDISTANT)
            
            self.camera_parameters_loaded = True
        else:
            self.camera_parameters_loaded = False
    
    def _get_cmd_str(self):
        cmd =  f"nvarguscamerasrc ! "
        cmd += f"video/x-raw(memory:NVMM), width={self.capture_width}, height={self.capture_height},"
        cmd += f" format=(string)NV12, framerate=(fraction){self.capture_fps}/1 ! nvvidconv ! video/x-raw,"
        cmd += f" width=(int){self.width}, height=(int){self.height}, format=(string)BGRx ! videoconvert ! appsink"
        return cmd
    
    def _correct_image(self, image):
        with vpi.Backend.CUDA:
            img_corrected = vpi.asimage(image)
            img_corrected = img_corrected.convert(vpi.Format.NV12_ER)
            img_corrected = img_corrected.remap(self.undist_map, interp=vpi.Interp.CATMULL_ROM)
            img_corrected = img_corrected.convert(vpi.Format.RGB8)
        
        return img_corrected.cpu()

    def read(self, fisheye_correction=False):
        re, image = self.cap.read()
        if not re:
            raise RuntimeError('Could not read image from camera')
        
        if fisheye_correction:
            if not self.camera_parameters_loaded:
                raise RuntimeError("Camera parameters are not loaded and fisheye correction option is enabled!")
            
            return self._correct_image(image)

        return image
