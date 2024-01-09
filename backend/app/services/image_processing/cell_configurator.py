# This module serves to the role to go from a whole sudoku image to its numpy form, by looking at individual cells
import cv2
import numpy as np
import matplotlib.pyplot as plt


def extract_all_cells(transformed_image, padding_amount=0.1):
    """
    Extracts individual cells from a Sudoku grid image.

    Parameters:
    - transformed_image: The perspective-transformed Sudoku grid image. (RGB)
    - padding_amount: padding fraction of cell size, to help remove any potential borders

    Returns:
    - cells: List of images, each representing an individual cell in the Sudoku grid.
    """

    # Calculate the size of each cell, include a negative padding for either side of the cell
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


def construct_sudoku_grid(cell_predictions, filled_cell_positions):
    """
    Constructs a 9x9 Sudoku grid with the predicted digits placed in the specified positions.

    Parameters:
    - cell_predictions: A NumPy array containing the predicted digits.
    - filled_cell_positions: A list of positions where the digits should be placed in the Sudoku grid.

    Returns:
    - sudoku_grid: A 9x9 NumPy array representing the filled Sudoku grid.
    """
    if len(cell_predictions) != len(filled_cell_positions):
        raise ValueError("The length of predictions and filled_cell_positions must be the same")

    # Initialize a 9x9 grid with zeros
    sudoku_grid = np.zeros((9, 9), dtype=int)

    # Place the predictions in their respective positions
    for pos, digit in zip(filled_cell_positions, cell_predictions):
        row = pos // 9  # Integer division to find the row
        col = pos % 9   # Modulus to find the column
        sudoku_grid[row, col] = digit

    return sudoku_grid
