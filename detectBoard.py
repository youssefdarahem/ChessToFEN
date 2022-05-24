import cv2 as cv
import numpy as np


def detectBoard(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Setting parameter values
    t_lower = 50  # Lower Threshold
    t_upper = 150  # Upper threshold

    # Applying the Canny Edge filter
    edge = cv.Canny(gray, t_lower, t_upper)
    lines = cv.HoughLines(edge, 1, np.pi/180, 150)
    if lines is not None:
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv.imshow('org', img)
    cv.imshow('edges', edge)
