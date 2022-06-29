import numpy as np

import cv2 as cv
from boardDetectFun import drawLines

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
    setup = True
    cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    # cap = cv.VideoCapture(0)
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 2
    color = (255, 0, 0)
    thickness = 2
    print('Press S to setup')

    while setup:
        ret, img = cap.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        edges = cv.Canny(gray, 100, 200, apertureSize=3)
        cv.imshow('img', img)
        cv.imshow('canny',edges)
        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('quiting')
            cap.release()
            break
        elif keyCode == ord('s'):
            # cv.imwrite('output/test.jpg',img)
            detectBoard(img)
            # print('Trying')
            print('Try agian ? (y/n)')
            choice = input()
            if choice == 'y':
                setup = True
            else:
                setup = False
    cap.release()
    cv.destroyAllWindows()


setup()
