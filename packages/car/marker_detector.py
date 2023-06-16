import cv2

class ArucoDetector:
    def __init__(self, aruco_dictionary=cv2.aruco.DICT_4X4_50):
        self.aruco_dict = cv2.aruco.Dictionary_get(aruco_dictionary)
        self.aruco_params = cv2.aruco.DetectorParameters_create()
    
    def detect_marker(self, img, marker_id = 0):
        corners, ids, _ = cv2.aruco.detectMarkers(img, self.aruco_dict, parameters=self.aruco_params)

        # Find marker with ID matching marker_id and calculate it's center coordinates
        if ids is not None:
            for i in range(len(ids)):
                if ids[i] == marker_id:
                    marker_center = (corners[i][0][0] + corners[i][0][2]) / 2
                    return marker_center
        return None
    



