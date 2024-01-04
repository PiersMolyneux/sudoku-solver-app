# This is the loader module for loading in datasets related to image processing
import cv2


def load_image(file_name: str):
    """
    Load an image from a specified file.

    Parameters:
    file_name (str): The path to the image file.

    Returns:
    np.ndarray: The loaded image in grayscale format, or None if loading fails.

    Raises:
    FileNotFoundError: If the file does not exist.
    """
    # Check if file exists
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file {file_name} does not exist.")

    # Load the image in grayscale
    original_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded successfully
    if original_image is None:
        print(f"Failed to load the image from {file_name}.")
        return None

    return original_image
