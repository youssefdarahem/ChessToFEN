from boardDetectFun import crop, readPoints, writeOutSquares
import numpy as np
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
    # img = cv.imread('inputs/test12P.jpeg')
    # img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    # # img = cv.flip(img, -1)
    # scale_percent = 40  # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    setup = True
    while setup:
        boardimg = []
        boardrow = []


        # resize image
        # resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        # shape = resized.shape
        points = readPoints()
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

        for i in range(8):
            for j in range(8):
                print(boardimg[i][j].position, end=" ")
            print()
        sqRow = []
        sqs = []
        for i in range(8):
            for j in range(8):
                sq = crop(img, boardimg[i][j])
                sqRow.append(sq)
            sqs.append(sqRow)
            sqRow = []
        

        cv.imshow('img', img)
        cv.imshow("croped", img)
        keyCode = cv.waitKey(10) & 0xFF
        if keyCode == ord('q'):
            print('quiting')
            cap.release()
            break
        elif keyCode == ord('s'):
            writeOutSquares(sqs,'./raw/',0)
            # print('Trying')
            print('countinue ? (y/n)')
            choice = input()
            if choice == 'y':
                setup = True
            else:
                setup = False

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
