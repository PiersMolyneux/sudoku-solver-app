from .model import sudokuCNN
# from ..histogram_matching import load_histogram, match_histogram
import os
import torch
import cv2
import numpy as np


def load_model(model_path=None):
    """
    Load a pre-trained Sudoku Convolutional Neural Network (CNN) model.

    This function initializes a CNN model for Sudoku digit recognition, loads its parameters from
    a specified file containing the model's state dictionary, and sets it to evaluation mode.

    Parameters:
    - model_path (str, optional): Path to the model's state dictionary file. If None, it defaults
      to 'sudoku_cnn_state_dict.pth' in the same directory as this script.

    Returns:
    - torch.nn.Module: The loaded PyTorch model in evaluation mode.

    Raises:
    - FileNotFoundError: If the state dictionary file does not exist at the specified path.

    Notes:
    - The 'sudokuCNN()' function used to instantiate the model must be defined in the same scope
      where 'load_model' is called.
    - The state dictionary file is expected to be compatible with the 'sudokuCNN' model architecture.
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


def predict_cell_digits(model, cells):
    """
    Use a trained model to predict the digit in each Sudoku cell image.

    The function converts a list of grayscale cell images into PyTorch tensors, feeds them into the
    provided model, and outputs the predicted digits. It assumes the model outputs logits for classes
    0-8, which correspond to digits 1-9.

    Parameters:
    - model (torch.nn.Module): The trained PyTorch model for digit prediction.
    - cells (list of numpy.ndarray): A list of preprocessed cell images represented as 2D NumPy arrays.

    Returns:
    - numpy.ndarray: An array of integers representing the predicted digits for each cell image.

    Raises:
    - ValueError: If 'model' is None or 'cells' is not a list of NumPy arrays.

    Notes:
    - Each cell image in the 'cells' list should be preprocessed to match the input requirements of the model.
    - The function adds two singleton dimensions to each cell image to match the expected input shape of the model.
    - Predictions are corrected by adding 1 to the output indices to shift from 0-indexing to 1-indexing (digits 1-9).
    """
    cells = [torch.tensor(cell, dtype=torch.float).unsqueeze(0).unsqueeze(0) for cell in cells]
    cells = torch.cat(cells, dim=0)

    if model is None or not isinstance(cells, torch.Tensor):
        raise ValueError("Invalid model or data type")

    model.eval()  # Ensure the model is in eval mode
    with torch.no_grad():
        outputs = model(cells)
        predictions = torch.argmax(outputs, dim=1)

    return predictions.numpy() + 1  # Model predicts 0-8, need to correct for our digits


