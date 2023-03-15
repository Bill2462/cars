# Zaadaptowano z : https://longervision.github.io/2017/03/16/ComputerVision/OpenCV/opencv-internal-calibration-chessboard/
import argparse
import cv2
import glob
import json
import os
import numpy as np
from tqdm import tqdm

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("imgdir", type=str,
                        help="Path to directory and containing images.")
    
    parser.add_argument("outfile", type=str,
                        help="Path to file where configuration will be saved.")

    parser.add_argument("--img_extension", type=str, default="png",
                        help="Image extension.")

    parser.add_argument("--chessboard_width", type=int, default=10,
                        help="Width of the chessboard (in number of fields).")

    parser.add_argument("--chessboard_height", type=int, default=7,
                        help="Height of chessboard (in number of fields).")

    parser.add_argument("--no_display", action="store_true",
                        help="Do not show images (much faster, use with large set of images).")

    return parser.parse_args()

def find_corners(img_filepaths, chessboard_size, show_images):
    corners_2D = []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for img_path in tqdm(img_filepaths):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        found, corners = cv2.findChessboardCorners(gray, chessboard_size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if found == True:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1,-1), criteria)
            corners_2D.append(corners)

            if show_images:
                cv2.drawChessboardCorners(img, chessboard_size, corners, found)

        if show_images:
            cv2.imshow("Image preview", img)
            cv2.waitKey(100)
        
    return corners_2D, gray.shape

def dump_config(filepath, cam_mtx, dist):
    data = {"camera_matrix": np.asarray(cam_mtx).tolist(), "dist_coeff": np.asarray(dist).tolist()}
    
    with open(filepath, "w") as f:
        json.dump(data, f)

def main():
    args = get_args()
    img_glob = os.path.join(args.imgdir, f"*.{args.img_extension}")
    chessboard_size = (args.chessboard_width-1, args.chessboard_height-1)
    image_filepaths = glob.glob(img_glob)

    corners_2D, img_shape = find_corners(image_filepaths, chessboard_size, not args.no_display)
    
    cb_corners = np.zeros((1, chessboard_size[0] * chessboard_size[1], 3))
    cb_corners[0,:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)
    corners_3D = [cb_corners.reshape(-1,1,3) for i in range(len(corners_2D))]

    print(f"Found {len(corners_2D)} correct images!")

    # Computing camera and distortion matrix.
    ret, cam_mtx, dist, rvecs, tvecs = cv2.fisheye.calibrate(corners_3D, corners_2D, img_shape[::-1], None, None)

    print("Camera matrix")
    print(cam_mtx)

    print("Distortion coeffixients: ")
    print(dist)

    dump_config(args.outfile, cam_mtx, dist)

    print("Camera parameters saved!")

if __name__ == "__main__":
    main()
