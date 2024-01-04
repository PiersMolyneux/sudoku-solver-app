# This is the cell_extractor module for extracting cells from an rgb sudoku, assuming it's been isolated
import cv2
import numpy as np



def extract_cells(transformed_image):
    """
    Extracts individual cells from a Sudoku grid image.

    Parameters:
    - transformed_image: The perspective-transformed Sudoku grid image. (RGB)

    Returns:
    - cells: List of images, each representing an individual cell in the Sudoku grid.
    """
    # Grayscale, blur, threshold image
    transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
    transformed_image = cv2.GaussianBlur(transformed_image, (5, 5), 0)
    _, transformed_image = cv2.threshold(transformed_image, 128, 255, cv2.THRESH_BINARY_INV)

    # Calculate the size of each cell, include a negative padding for the cell
    padding_amount = 0.05  # padding percentage of cell size
    cell_height = transformed_image.shape[0] // 9
    cell_height_padding = int(cell_height * padding_amount)
    cell_width = transformed_image.shape[1] // 9
    cell_width_padding = int(cell_width * padding_amount)

    cells = []
    for row in range(9):
        for col in range(9):
            # Calculate the start and end coordinates for each cell
            start_y = row * cell_height
            end_y = (row + 1) * cell_height
            start_x = col * cell_width
            end_x = (col + 1) * cell_width

            # Extract and store the cell, remove cell borders so sudoku grid lines do not interfere
            cell = transformed_image[start_y : end_y, start_x : end_x]
            cell = cell[cell_height_padding : cell_height - cell_height_padding,
                         cell_width_padding : cell_width - cell_width_padding]
            cells.append(cell)

    return cells



def is_filled(cell, threshold_percentage=0.01):
    """
    Determine whether a cell is filled based on the number of white pixels.

    Parameters:
    - cell: The thresholded image of the cell (white digit on black background).
    - white_pixel_threshold: The threshold of white pixels to determine if a cell is filled.

    Returns:
    - True if the cell is filled, False otherwise.
    """
    # Assuming the cell image is binary (i.e., the digit is white, the background is black)
    white_pixel_threshold = cell.size * threshold_percentage
    white_pixels = cv2.countNonZero(cell)
    
    # If the number of white pixels exceeds the threshold, the cell is likely filled
    return white_pixels > white_pixel_threshold
