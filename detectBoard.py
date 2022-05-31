import cv2 as cv
import numpy as np
from boardDetectFun import *


def detectBoard(img, shape):

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    t_lower = 100  # Lower Threshold
    t_upper = 200  # Upper threshold

    edges = cv.Canny(gray, t_lower, t_upper, apertureSize=3)
    # lines = cv.HoughLinesP(
    #     edges,  # Input edge image
    #     1,  # Distance resolution in pixels
    #     np.pi/180,  # Angle resolution in radians
    #     threshold=50,  # Min number of votes for valid line
    #     minLineLength=10,  # Min allowed length of line
    #     maxLineGap=60  # Max allowed gap between line for joining them
    # )

    lines = cv.HoughLines(edges, 1, np.pi/180, 160)
    h_lines, v_lines = h_v_lines(lines)
    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)
    points2 = augment_points(points)
    point3 = boardPoints(points)
    arrP = np.array(points)
    start_y = arrP[0][1]
    end_y = arrP[-1][1]
    xy = np.transpose(arrP)
    start_x = min(xy[0])
    end_x = max(xy[0])
    print(start_y)
    print(end_y)
    print(start_x)
    print(end_x)
    # print(arrP)

    # Todo: find a way to return only the points of the chess board

    for point in points:
        x = np.array(point)

        x = x.astype(int)

        point = tuple(x)
        cv.circle(img, point, 1, (0, 0, 255), 2)

    # for point in points:
    #     x = np.array(point)

    #     x = x.astype(int)

    #     point = tuple(x)
    #     cv.circle(img, point, 1, (255, 0, 255), 2)
        # if(x[1] > (end_y - start_y)//2 and x[1] < ((end_y - start_y)//2)+40):
        #     cv.circle(img, point, 1, (255, 0, 255), 2)
        #     if(x[0] > (abs(end_x - start_x))//2 and x[0] < ((abs(end_x - start_x))//2)+70):
        #         cv.circle(img, point, 1, (0, 255, 255), 2)
        # else:
        #     cv.circle(img, point, 1, (0, 0, 255), 2)
    # drawLines(img, lines)

    cv.imshow('org', img)
    cv.imshow('edges', edges)
