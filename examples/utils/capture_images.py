import cv2
import os
import time
import argparse
import sys
import select
from car.camera import CSICamera
from car.telemetry import TelemetrySender

def check_if_enter_pressed():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.read(1)
        return True
    return False

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("outdir", type=str,
                        help="Path where images will be saved.")

    parser.add_argument("--recording_len", type=float, default=120,
                        help="Length of the recording in seconds.")

    parser.add_argument("--preview_topic", type=str, default="img",
                        help="Name of the output image channel.")

    parser.add_argument("--image_extension", type=str, default="png",
                        help="Image extension.")

    parser.add_argument("--single_shot", action="store_true",
                        help="If this is set the program will wait for press of enter key to capture an image.")
    
    parser.add_argument("--camera_params_filepath", type=str,
                        help="If this is set to camera parameters filepath, lens distortion correction will be performed.")

    return parser.parse_args()

def main():
    args = get_args()
    
    # Ensure that output directory exists.
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    if args.camera_params_filepath:
        cam = CSICamera(camera_parameters_filepath = args.camera_params_filepath)
        fisheye_correction = True
    else:
        cam = CSICamera()
        fisheye_correction = False

    telemetry = TelemetrySender()

    print("Starting capture of images...")
    end_timestamp = time.time() + args.recording_len
    idx = 0

    if args.single_shot:
        print("Press ctrl+c to exit and enter to capture still image")
        while 1:
            img = cam.read(fisheye_correction)
            if check_if_enter_pressed():
                cv2.imwrite(os.path.join(args.outdir, f"{idx}.{args.image_extension}"), img)
                idx +=1
                print(f"Captured frame {idx}")
            
            telemetry.log_image(args.preview_topic, img)

    while time.time() < end_timestamp:
        img = cam.read(fisheye_correction)
        cv2.imwrite(os.path.join(args.outdir, f"{idx}.{args.image_extension}"), img)

        telemetry.log_image(args.preview_topic, img)
        idx += 1

    print("Capture done!")

if __name__ == "__main__":
    main()
