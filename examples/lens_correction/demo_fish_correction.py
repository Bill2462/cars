import argparse
import numpy as np
from car.camera import CSICamera, load_camera_parameters
from car.telemetry import Telemetry
import vpi # Has to be imported after opencv (import last just to be save).

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("camera_parameters_filepath", type=str,
                        help="Path to camera parameters file.")

    parser.add_argument("--uncorrected_img_topic", type=str, default="img",
                        help="Uncorrected image topic.")

    parser.add_argument("--corrected_img_topic", type=str, default="img_uncorrected",
                        help="Corrected image topic.")

    return parser.parse_args()

def main():
    args = get_args()

    cam = CSICamera()
    telemetry = Telemetry()

    cam_matrix, dist_coeff = load_camera_parameters(args.camera_parameters_filepath)

    # Create an uniform grid
    grid = vpi.WarpGrid((cam.width, cam.height))
  
    # Create undistort warp map from the calibration parameters and the grid
    undist_map = vpi.WarpMap.fisheye_correction(grid,
                                                K=cam_matrix[0:2,:],
                                                X=np.eye(3,4),
                                                coeffs=dist_coeff,
                                                mapping=vpi.FisheyeMapping.EQUIDISTANT)

    while 1:
        img = cam.read()
        with vpi.Backend.CUDA:
            img_corrected = vpi.asimage(img)
            img_corrected = img_corrected.convert(vpi.Format.NV12_ER)
            img_corrected = img_corrected.remap(undist_map, interp=vpi.Interp.CATMULL_ROM)
            img_corrected = img_corrected.convert(vpi.Format.RGB8)
        
        telemetry.log_image(args.corrected_img_topic, img_corrected.cpu())
        telemetry.log_image(args.uncorrected_img_topic, img)

if __name__ == "__main__":
    main()
