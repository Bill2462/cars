import cv2
import os
import time
import argparse
from car.camera import CSICamera
from car.telemetry import Telemetry

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

    return parser.parse_args()

def main():
    args = get_args()
    
    # Ensure that output directory exists.
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    cam = CSICamera()
    telemetry = Telemetry()

    print("Starting capture of images...")
    end_timestamp = time.time() + args.recording_len
    idx = 0

    while time.time() < end_timestamp:
        img = cam.read()
        cv2.imwrite(os.path.join(args.outdir, f"{idx}.{args.image_extension}"), img)

        telemetry.log_image(args.preview_topic, img)
        idx += 1

    print("Capture done!")

if __name__ == "__main__":
    main()
