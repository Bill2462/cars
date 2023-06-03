import numpy as np
import tensorrt as trt
import pycuda.autoprimaryctx
import pycuda.driver as cuda
import os
from car.camera import CSICamera
from car.telemetry import TelemetrySender
import cv2

telemetry = TelemetrySender()
cam = CSICamera()

def main():

    ### Kod wykonywany raz
    
    while 1:
        frame = cam.read()

        # Kod do inferencji modelu

        ## Podgląd kamery
        telemetry.log_image("img", frame)

if __name__ == '__main__':
    main()
