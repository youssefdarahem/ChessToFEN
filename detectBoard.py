import cv2 as cv
from cv2 import threshold
import numpy as np
from boardDetectFun import *


def detectBoard(img, shape):
    min_area = 200000
    max_area = 10000000
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    edges = cv.Canny(gray, 100, 200, apertureSize=3)
    cnts = cv.findContours(
        edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    idx = 0
    for points in cnts:
        area = cv.contourArea(points)
        print(area)

        if area > min_area and area < max_area:
            # cv.drawContours(img, cnts, idx, 255, 2)
            # cornerPoints = drawExtractsquare(img, points)
            break
        idx += 1
        
    
    mask = np.zeros_like(img)
    cv.drawContours(mask, cnts, idx, (255, 255, 255), -1)
    masked_image = cv.bitwise_and(img, mask)
    cv.imshow('mask', masked_image)
    
    ## Extract out the object and place into output image

    # (x, y) = np.where(mask == 255)
    # print(x)
    # (topy, topx) = (np.min(y), np.min(x))
    # (bottomy, bottomx) = (np.max(y), np.max(x))
    # out = out[topy:bottomy+1, topx:bottomx+1]

    # cv.imshow('output', out)
    # p1, p2, p3, p4 = cornerPoints.points

    # cv.line(img, p1, p2, (255, 255, 255), 2)
    # cv.line(img, p3, p2, (255, 255, 255), 2)
    # cv.line(img, p4, p3, (255, 255, 255), 2)
    # cv.line(img, p1, p4, (255, 255, 255), 2)
    # mask = np.ones(img.shape, dtype=np.uint8)
    # mask.fill(255)
    # # points to be cropped
    # roi_corners = np.array([cornerPoints.points], dtype=np.int32)
    # # fill the ROI into the mask
    # cv.fillPoly(mask, roi_corners, 0)

    # # applying th mask to original image
    # masked_image = cv.bitwise_or(img, mask)
    # cv.imshow('cropped', masked_image)

    gray = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(masked_image, 50, 200, apertureSize=3)

    lines = cv.HoughLines(edges, 1, np.pi/180, 160)
    h_lines, v_lines = h_v_lines(lines)
    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)
    center = (int(img.shape[1]/2), int(img.shape[0]/2))
    newPoints = removeClosePoints(points, center, threshhold=40)
    if (len(newPoints) == 81):
        print('it seems like a good fit!!')
        allrows = organizeSave(newPoints)
        print(len(allrows))
    else:
        print('try to position the baord differently')
    pointsFromTxt = readPoints()
    drawOrderedPoints(img, pointsFromTxt)

    cv.imshow('canny', edges)
    cv.imshow('image', img)
    cv.waitKey()
