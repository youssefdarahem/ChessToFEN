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
    setup = True
    # cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    cap = cv.VideoCapture(0)
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 2
    color = (255, 0, 0)
    thickness = 2

    while setup:
        ret, img = cap.read()
        cv.putText(img, 'press s to setup', org,
                   font, fontScale, color, thickness)
        cv.imshow('img', img)
        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('quiting')
            cap.release()
            break
        elif keyCode == ord('s'):
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
