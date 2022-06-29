from boardDetectFun import crop, drawOrderedPoints, readPoints, writeOutSquares
import numpy as np
from defmodel import myModel
from square import Square
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
  

    cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
    ret, img = cap.read()
   
    setup = True
    boardimg = []
    boardrow = []

    boardimg = []
    boardrow = []
    index = 0

    points = readPoints()

    for i in range(9):
        points[i] = sorted(points[i], reverse=True)

    squareid = 64

    for i in range(8):
        for j in range(8):
            p1 = points[i][j]
            p2 = points[i][j+1]
            p3 = points[i+1][j]
            p4 = points[i+1][j+1]
            square = Square(p1=p1, p2=p2, p3=p3, p4=p4, position=squareid)
            squareid -= 1
            boardrow.append(square)
        boardimg.append(boardrow)
        boardrow = []

    boardimg = np.transpose(boardimg)
    boardimg = np.flip(boardimg, 1)
    boardimg = np.flip(boardimg, 0)

    squareid = 1
    for i in range(8):
        for j in range(8):
            boardimg[i][j].position = squareid
            squareid += 1

    index = 0
    while setup:
        sqRow = []
        sqs = []
        for i in range(8):
            for j in range(8):
                sq = crop(img, boardimg[i][j])
                sqRow.append(sq)
            sqs.append(sqRow)
            sqRow = []


        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('quiting')
            cap.release()
            break
        elif keyCode == ord('s'):
            writeOutSquares(sqs,'./raw/',index=index)
            print('countinue ? (y/n)')
            choice = input()
            if choice == 'y':
                ret, img = cap.read()
                index += 64
                setup = True

            else:
                setup = False

        break
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
