import cv2 as cv
def detectBoard(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Setting parameter values
    t_lower = 50  # Lower Threshold
    t_upper = 150  # Upper threshold
  
    # Applying the Canny Edge filter
    edge = cv.Canny(gray, t_lower, t_upper)
    cv.imshow('edges',edge)
