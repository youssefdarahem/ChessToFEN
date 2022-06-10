from hashlib import new
import cv2 as cv
import numpy as np
from boardDetectFun import *


def detectBoard(img, shape):
    min_area = 1000
    max_area = 1000000
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 200, apertureSize=3)
    # Find contours and filter using threshold area
    cnts = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for points in cnts:
        area = cv.contourArea(points)
        if area > min_area and area < max_area:
            cornerPoints = drawExtractsquare(img, points)

    p1, p2, p3, p4 = cornerPoints.points

    cv.line(img, p1, p2, (255, 255, 255), 2)
    cv.line(img, p3, p2, (255, 255, 255), 2)
    cv.line(img, p4, p3, (255, 255, 255), 2)
    cv.line(img, p1, p4, (255, 255, 255), 2)
    mask = np.ones(img.shape, dtype=np.uint8)
    mask.fill(255)
    # points to be cropped
    roi_corners = np.array([cornerPoints.points], dtype=np.int32)
    # fill the ROI into the mask
    cv.fillPoly(mask, roi_corners, 0)

    # applying th mask to original image
    masked_image = cv.bitwise_or(img, mask)
    cv.imshow('cropped', masked_image)

    gray = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(masked_image, 50, 200, apertureSize=3)

    lines = cv.HoughLines(edges, 1, np.pi/180, 160)
    h_lines, v_lines = h_v_lines(lines)
    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)
    center = (int(img.shape[1]/2), int(img.shape[0]/2))
    newPoints = removeClosePoints(points, center, cornerPoints, threshhold=40)
    if (len(newPoints) == 81):
        print('it seems like a good fit!!')
        allrows = organizeSave(newPoints)
        print(len(allrows))
    else:
        print('try to position the baord differently')
    pointsFromTxt = readPoints()
    for i in range(9):
        drawPoints(img, allrows[i])

    cv.imshow('canny', edges)
    cv.imshow('image', img)
    cv.waitKey()
