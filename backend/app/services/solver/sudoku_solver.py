import numpy as np


#  Main function
def solve_sudoku(sudoku):
    """
    Solves a Sudoku puzzle using a backtracking algorithm.

    Parameters:
     - sudoku (numpy array): A 9x9 numpy array representing the Sudoku grid,
                            where 0 indicates an empty cell.

    Returns:
     - boolean: True if the Sudoku puzzle is solved, False if it cannot be solved.
    """
    empty_cell = find_next_empty_cell(sudoku)
    if empty_cell is None:
        return True  # Sudoku solved

    row, col = empty_cell

    for value in range(1, 10):
        if is_valid_placement(sudoku, row, col, value):
            sudoku[row, col] = value
            if solve_sudoku(sudoku):
                return True
            sudoku[row, col] = 0  # Backtrack

    return False  # Backtrack if no valid number found


# Supplementary functions 
def find_next_empty_cell(sudoku):
    """
    Finds the next empty cell (with a value of 0) in the Sudoku grid.

    Parameters:
     - sudoku (numpy array): The Sudoku grid.

    Returns:
     - tuple: The row and column index of the next empty cell, or None if no empty cell is found.
    """
    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                return row, col
    return None


def is_valid_placement(sudoku, row, col, value):
    """
    Checks if placing a value in a specified cell is valid according to Sudoku rules.

    Parameters:
     - sudoku (numpy array): The Sudoku grid.
     - row (int): Row index of the cell.
     - col (int): Column index of the cell.
     - value (int): The value to check.

    Returns:
     - boolean: True if the placement is valid, False otherwise.
    """
    # Check row and column
    if value in sudoku[row, :] or value in sudoku[:, col]:
        return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    subgrid = sudoku[start_row:start_row + 3, start_col:start_col + 3]
    if value in subgrid:
        return False

    return True
