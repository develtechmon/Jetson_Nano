import numpy as np
import cv2

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int)%d, height=(int)%d, "
    "format=(string)NV12, framerate=(fraction)%d/1 ! "
    "nvvidconv flip-method=%d ! "
    "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
    % (
        capture_width,
        capture_height,
        framerate,
        flip_method,
        display_width,
        display_height,
    )
)


def gstreamer_pipeline_csi(
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


def show_camera():
    cap = cv2.VideoCapture(gstreamer_pipeline_csi(flip_method=6), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        while True:
            success, img = cap.read()
            cv2.imshow("Capture", img)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")
    
#    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
#    print(gstreamer_pipeline(flip_method=0))
#    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#    if cap.isOpened():
#        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
#        # Window
#        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
#            ret_val, img = cap.read()
#            cv2.imshow("CSI Camera", img)
#            # This also acts as
#            keyCode = cv2.waitKey(30) & 0xFF
#            # Stop the program on the ESC key
#            if keyCode == 27:
#                break
#        cap.release()
#        cv2.destroyAllWindows()
#    else:
#        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
    
