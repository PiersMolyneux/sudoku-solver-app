# This is the loader module for loading in datasets related to image processing
import os
import cv2


def load_image(file_name: str):
    """
    Load an image from a specified file.

    Parameters:
    file_name (str): The path to the image file.

    Returns:
    np.ndarray: The loaded image in RGB format, or None if loading fails.

    Raises:
    FileNotFoundError: If the file does not exist.
    """
    # Check if file exists
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file {file_name} does not exist.")

    # Load the image in RGB
    image = cv2.imread(file_name, cv2.IMREAD_COLOR)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Failed to load the image from {file_name}.")
        return None

    return image
