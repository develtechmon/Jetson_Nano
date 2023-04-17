import jetson.inference
import jetson.utils
import cv2
from video_capture import *

from csi_camera import CSI_Camera

class Camera:
    def __init__(self):
        self.net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        self.DISPLAY_WIDTH=640
        self.DISPLAY_HEIGHT=480
        
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline_csi(flip_method=6), cv2.CAP_GSTREAMER)

    def gstreamer_pipeline_csi(
        self,
        sensor_id=0,
        sensor_mode=3,
        display_width=640,
        display_height=480,
        framerate=30,
        flip_method=6,
    ):
        return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
        sensor_id,
        sensor_mode,
        framerate,
        flip_method,
        display_width,
        display_height,
        )
    )


    

