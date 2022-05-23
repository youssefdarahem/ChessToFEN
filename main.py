from camera import Camers
from detectBoard import detectBoard

import cv2 as cv


def main():
    camera = Camers(nano_Camera=False)
    cap = camera.use()
    while True:
        ret, img = cap.read()
        detectBoard(img=img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
