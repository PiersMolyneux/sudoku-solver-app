# This is the preprocessor module for loading in sudoku images belonging to the image_processing package 

import cv2
import numpy as np


def blur_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def threshold_image(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

def find_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def sudoku_detection(image):

    # Apply Gaussian blur to image, reducing noise
    blurred = blur_image(image)

    # Apply adaptive thresholding to binarize image
    thresh = threshold_image(blurred)

    # Find image contours
    contours = find_contours(thresh)

    # Assume the largest contour is the Sudoku grid
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the perimeter of the contour
    perimeter = cv2.arcLength(largest_contour, True)

    # Approximate the corners of the grid
    approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)

    # If we have four points, then we have found the grid
    if len(approx) == 4:
        # Get the top-down view of the Sudoku grid
        top_down_view = four_point_transform(image, approx.reshape(4, 2))
        
        # Now, top_down_view holds the isolated Sudoku grid
        # You can save or display the image
        cv2.imshow('Sudoku Grid', top_down_view)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Grid not detected.")



