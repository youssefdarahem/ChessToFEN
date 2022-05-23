import cv2 as cv
class Camers():

    def __init__(self,nano_Camera = True):
        self.nano_Camera = nano_Camera

    def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=960,
    display_height=540,
    framerate=120,
    flip_method=0,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink drop=True"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )

    def use(self):
        if self.nano_Camera:
            cap = cv.VideoCapture(self.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        else:
            cap =  cv.VideoCapture(0)
        return cap
        
