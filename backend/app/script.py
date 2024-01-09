import logging
from services.image_processing.loader import load_image
from services.image_processing.image_preprocessor import isolate_sudoku
from services.image_processing.cell_configurator import extract_all_cells, construct_sudoku_grid
from services.image_processing.cell_preprocessor import preprocess_and_select_cells
from services.image_processing.digit_recognition.tools import predict_cell_digits, load_model
from services.solver.sudoku_solver import solver

# Configure logging
logging.basicConfig(level=logging.INFO)

DEFAULT_IMAGE_PATH = '../data/sudoku_tests/sudoku_test2.png'

def load(path=DEFAULT_IMAGE_PATH):
    """
    Load the image from the given path.
    
    Parameters:
    path (str): The path to the image file.

    Returns:
    numpy.ndarray: The loaded image.
    """
    return load_image(path)

def process_image(image):
    """
    Process the given image to extract sudoku grid in a format ready for solving.

    Parameters:
    image (numpy.ndarray): The image containing the sudoku puzzle.

    Returns:
    numpy.ndarray: 2D array representing the sudoku grid with digits.
    """
    try:
        transformed_image = isolate_sudoku(image)
        sudoku_cells = extract_all_cells(transformed_image)
        filled_sudoku_cells, filled_cell_positions = preprocess_and_select_cells(sudoku_cells)
        model = load_model()
        predictions = predict_cell_digits(model, filled_sudoku_cells)
        grid = construct_sudoku_grid(predictions, filled_cell_positions)
        return grid
    except Exception as e:
        logging.error(f"Error occurred during image processing: {e}", exc_info=True)
        raise

def solve(grid):
    """
    Solve the given sudoku grid.

    Parameters:
    grid (numpy.ndarray): 2D array representing the sudoku grid with digits.

    Returns:
    numpy.ndarray: Solved sudoku grid.
    """
    try:
        if solver(grid):
            return grid
        else:
            raise ValueError("Could not solve sudoku")
    except Exception as e:
        logging.error(f"Error occurred during solving sudoku: {e}", exc_info=True)
        raise

def test_workflow():
    """
    Function to test the complete workflow from loading an image to solving the sudoku.
    """
    try:
        image = load()
        grid = process_image(image)
        solved_grid = solve(grid)
        logging.info(f"Solved Sudoku Grid:\n{solved_grid}")
    except Exception as e:
        logging.error("Failed to complete the sudoku solving workflow.", exc_info=True)


if __name__ == '__main__':
    test_workflow()
