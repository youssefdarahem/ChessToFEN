from camera import Camers
from detectBoard import detectBoard

import cv2 as cv


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


def main():
    # cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    # camera = Camers(nano_Camera=False)
    # cap = camera.use()

    # ret, img = cap.read()
    img = cv.imread('inputs/test5.jpeg')
    scale_percent = 40  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

# resize image
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    shape = resized.shape
    detectBoard(img=resized, shape=shape)
    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break
    # cap.release()
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
