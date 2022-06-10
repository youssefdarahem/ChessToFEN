import cv2 as cv

from detectBoard import detectBoard


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


def setup():
    cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    while True:
        ret, img = cap.read()
        cv.imshow(img)
        cv.addText(img, 'press s to setup', (0, 0))
        if cv.waitKey(0):
            detectBoard(img)
