from model import sudokuCNN
import os
import torch
import cv2



# Main Functions:


def predict_cell_digits(model, cells):
    """
    Predicts the digit in each cell using the provided model.

    Parameters:
     - model: Trained PyTorch model for digit prediction.
     - cells: List of cell images as 2D NumPy arrays.

    Returns: 
     - predictions: Predicted digits as a NumPy array.
    """
    preprocessed_cells = prepare_cells_for_prediction(cells)  # Preparing cells for prediction into single tensor

    if model is None or not isinstance(preprocessed_cells, torch.Tensor):
        raise ValueError("Invalid model or preprocessed_cells")

    model.eval()  # Ensure the model is in eval mode
    with torch.no_grad():
        outputs = model(preprocessed_cells)
        predictions = torch.argmax(outputs, dim=1)

    return predictions.numpy() + 1  # Model predicts 0-8, need to correct for our digits




# Supplementary functions:

def prepare_cells_for_prediction(cells):
    """
    Prepare a batch of sudoku cell images for prediction.
    Each image is preprocessed and combined into a single tensor.

    Parameters:
     - cells: List of cell images as 2D NumPy arrays.

    Returns: 
     - A batch of preprocessed images as a PyTorch tensor.
    """
    if not cells or not isinstance(cells, list):  
        raise ValueError("cells must be a non-empty list of images")

    preprocessed_cells = [preprocess_image(cell) for cell in cells]
    return torch.cat(preprocessed_cells, dim=0)


def preprocess_image(image):
    """
    Preprocesses a single image for model prediction.
    The image is resized, normalized, and converted to a PyTorch tensor.

    Parameters:
     - image: Input image as a 2D NumPy array.

    Returns: 
     - Preprocessed image as a PyTorch tensor.
    """
    if image is None or image.ndim != 2:
        raise ValueError("image must be a 2D NumPy array")

    # Resize to 28x28 and Normalize
    resized_image = cv2.resize(image, (28, 28))
    normalized_image = (resized_image / 255.0 - 0.5) / 0.5  # Same normalisation as training

    return torch.tensor(normalized_image, dtype=torch.float).unsqueeze(0).unsqueeze(0)



def load_model(model_path=None):
    """
    Loads the trained Sudoku CNN model from a given state dictionary path.

    Parameters:
     - model_path: Path to the model's state dictionary file. 
                       If None, defaults to the same directory as this script.
    Returns: 
     - Loaded and evaluated PyTorch model.
    """
    if model_path is None:
        # Get the directory of the current file and append the default filename
        directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(directory, "sudoku_cnn_state_dict.pth")

    try:
        state_dict = torch.load(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}")

    model = sudokuCNN()
    model.load_state_dict(state_dict)
    model.eval()
    return model



