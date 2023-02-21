import traitlets
from traitlets.config.configurable import SingletonConfigurable
import atexit
import cv2
import threading
import numpy as np

class OpenCvGstCamera(SingletonConfigurable):
    value = traitlets.Any()

    # config
    width = traitlets.Integer(default_value=224).tag(config=True)
    height = traitlets.Integer(default_value=224).tag(config=True)
    fps = traitlets.Integer(default_value=21).tag(config=True)
    capture_width = traitlets.Integer(default_value=640).tag(config=True)
    capture_height = traitlets.Integer(default_value=480).tag(config=True)

    def __init__(self, *args, **kwargs):
            self.value = np.empty((self.height, self.width, 3), dtype=np.uint8)
            super(OpenCvGstCamera, self).__init__(*args, **kwargs)
            try:
                self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
                re, image = self.cap.read()
                if not re:
                    raise RuntimeError('Could not read image from camera.')
                self.value = image
                self.start()
            except:
                self.stop()
                raise RuntimeError('Could not initialize camera.  Please see error trace.')
            atexit.register(self.stop)

    def _capture_frames(self):
        while True:
            re, image = self.cap.read()
            if re:
                self.value = image
            else:
                break
                
    def _gst_str(self):
        return 'v4l2src ! video/x-raw, width=640, height=480, format=(string)YUY2, framerate=(fraction)30 ! nvvidconv ! video/x-raw(memory:NVMM) ! nvvidconv ! video/x-raw, width=(int)224, height=(int)224, format=(string)BGRx ! videoconvert ! appsink'
    
    def start(self):
        if not self.cap.isOpened():
            self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
            if hasattr(self, 'cap'):
                self.cap.release()
            if hasattr(self, 'thread'):
                self.thread.join()
            
    def restart(self):
        self.stop()
        self.start()
