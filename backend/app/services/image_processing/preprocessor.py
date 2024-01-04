# This is the preprocessor module for preprocessing the sudoku image and isolating it
import os
import cv2
import numpy as np


# Main function :
def isolate_sudoku(image):
    """
    Perform a perspective transform to obtain a top-down view of an image and isolate the sudoku.

    Parameters:
    - image: Original image.

    Returns:
    - transformed_image: The perspective-transformed image.
    """
    # Find the corners of the sudoku, order them, figure out height and width of sudoku within image.
    corners = get_sudoku_corners(image) 
    ordered_points = order_points(corners.reshape(4, 2))
    maxWidth, maxHeight = calculate_dimensions(ordered_points)

    # Construct destination points for perspective transform
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # Apply perspective transform
    transform_matrix = cv2.getPerspectiveTransform(ordered_points, dst)
    transformed_image = cv2.warpPerspective(image, transform_matrix, (maxWidth, maxHeight))

    return transformed_image




# Suplementary functions :

def get_sudoku_corners(image):
    """
    Detect the corners of the Sudoku grid in the image.

    Parameters:
    - image: Original Sudoku image in BGR color format.

    Returns:
    - Approximated corner points of the Sudoku grid if detected, else None.
    """
    # Greyscale, blur, threshold image 
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
    
    # Find image contours. Largest contour should be the sudoku
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
  
    # Get the perimeter of the largest contour
    perimeter = cv2.arcLength(largest_contour, True)

    # Approximate the corners of the largest contour
    corners = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)

    if len(corners) == 4:
        return corners
    else:
        print("Sudoku grid not detected.")
        return None


def order_points(corner_pts):
    """
    Order corner points/coordinates in a specific order: top-left, top-right, bottom-right, bottom-left.

    Parameters:
    - corner_pts: The array of contour points.

    Returns:
    - ordered_points: Ordered array of corner points.
    """
    ordered_points = np.zeros((4, 2), dtype='float32')
    sum_pts = corner_pts.sum(axis=1)
    ordered_points[0] = corner_pts[np.argmin(sum_pts)]  # Top-left point has the smallest sum
    ordered_points[2] = corner_pts[np.argmax(sum_pts)]  # Bottom-right point has the largest sum

    diff_pts = np.diff(corner_pts, axis=1)
    ordered_points[1] = corner_pts[np.argmin(diff_pts)]  # Top-right point has the smallest difference
    ordered_points[3] = corner_pts[np.argmax(diff_pts)]  # Bottom-left point has the largest difference

    return ordered_points


def calculate_dimensions(ordered_points):
    """
    Calculate the dimensions of the new transformed image.

    Parameters:
    - ordered_points: Points in the order [top-left, top-right, bottom-right, bottom-left]

    Returns:
    - maxWidth: The width of the transformed image.
    - maxHeight: The height of the transformed image.
    """
    (tl, tr, br, bl) = ordered_points  # e.g. tl = top left

    # Width calculations
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    # Height calculations
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    return maxWidth, maxHeight


