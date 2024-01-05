# This is the cell_extractor module for extracting cells from an rgb sudoku, assuming it's been isolated. We also determine if a sudoku cell is filled
import cv2
import numpy as np


#  Main functions

def extract_all_cells(transformed_image):
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

    # We want grayscale, not binary, hence apply a mask to remove noisy background, but keep the digit values
    _, mask = cv2.threshold(transformed_image, 128, 1, cv2.THRESH_BINARY_INV)
    transformed_image = transformed_image * mask

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



def isolate_filled_cells(cells, filled_pixel_threshold_fraction=0.01):
    """
    Isolates filled cells from a list of cell images and keeps track of their original positions.

    Parameters:
    - cells: A list of grayscale sudoku cell images.
    - filled_pixel_threshold_fraction: The threshold percentage of filled pixels to determine if a cell is filled.

    Returns:
    - filled_cells: A list of filled cell images.
    - filled_cell_positions: The corresponding positions of filled cells in the original list.
    """
    filled_cells = []
    filled_cell_positions = []

    for i, cell in enumerate(cells):
        if is_filled(cell, filled_pixel_threshold_fraction): 
            filled_cells.append(cell)
            filled_cell_positions.append(i)
    
    return filled_cells, filled_cell_positions




# Supplementary functions

def is_filled(cell, filled_pixel_threshold_fraction=0.01):
    """
    Determine whether a cell is filled based on the number of sufficiently bright pixels in a grayscale image.

    Parameters:
    - cell: The grayscale image of the cell, where background noise has been removed
    - filled_pixel_threshold_fraction: The threshold percentage of filled pixels to determine if a cell is filled.

    Returns:
    - True if the cell is filled, False otherwise.
    """

    # Count pixels with intensity higher than the threshold, choose an arbituary low threshold as background has been removed
    intensity_threshold = 50
    bright_pixels = np.sum(cell > intensity_threshold)

    # Calculate the total number of pixels, and percentage of bright pixels
    total_pixels = cell.size
    bright_pixel_percentage = bright_pixels / total_pixels

    # Determine if the cell is filled based on the percentage
    return bright_pixel_percentage > filled_pixel_threshold_fraction


