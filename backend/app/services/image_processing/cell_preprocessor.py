import cv2
import numpy as np
import os


def preprocess_and_select_cells(cells):
    """
    Process and filter a batch of Sudoku cell images to be ready for digit prediction.

    This function takes a list of RGB cell images, applies preprocessing to each image,
    and selects only those that are filled with a digit. Each image is processed using the
    `preprocess_sudoku_cell` function, which must be defined elsewhere in the code. The output
    is a tuple containing a list of preprocessed cell images ready for prediction and a list of
    their corresponding indices in the original batch.

    Parameters:
    - cells (list of numpy.ndarray): A list of cell images represented as 3D (RGB) NumPy arrays.

    Returns:
    - tuple of (list of numpy.ndarray, list of int):
        - selected_cells: A list of NumPy arrays representing the preprocessed cell images that contain digits.
        - indices: A list of integers indicating the original positions of the selected cells in the input list.

    Raises:
    - ValueError: If 'cells' is not a non-empty list of images.

    Notes:
    - The function assumes that all images in the 'cells' list are RGB images of the same dimension and that they
      represent individual Sudoku cells.
    - The preprocessing steps typically include grayscaling, thresholding, noise removal, and other transformations
      necessary for preparing the images for a prediction model.
    """
    if not cells or not isinstance(cells, list):  
        raise ValueError("cells must be a non-empty list of images")

    selected_cells = []
    indices = []
    for i, cell in enumerate(cells):
        preprocessed_cell = preprocess_sudoku_cell(cell)
        if preprocessed_cell is not None:
            selected_cells.append(preprocessed_cell)
            indices.append(i)
            
    return selected_cells, indices




def preprocess_sudoku_cell(cell_image): 
    """    
    Preprocess a Sudoku cell image for digit recognition.

    This function converts an RGB image of a Sudoku cell to grayscale, applies Gaussian blur to
    smooth the image, and normalizes the pixel intensity values. It also performs thresholding to
    remove the background and adjusts the image contrast by clipping the pixel intensity values
    based on calculated percentiles. If a digit is detected within the cell, additional processing
    steps include border removal, digit centering, resizing, histogram matching, and normalization
    for consistency with the MNIST dataset preprocessing. If no digit is detected we return None.

    The output is a 28x28 pixel image normalized in the same manner as the MNIST training data,
    suitable for use with a digit recognition model.

    Parameters:
    - cell_image (numpy.ndarray): An RGB image of a Sudoku cell.

    Returns:
    - numpy.ndarray or None: A 28x28 pixel preprocessed image of a Sudoku cell if a digit is
      detected, or None if the cell is empty.

    Preconditions:
    - is_filled(cell_image): A function that determines if the cell contains a digit.
    - remove_border(cell_image): A function that removes the border from the cell image.
    - centre_digit(cell_image): A function that centers the digit within the image.
    - match_histogram(cell_image): A function that matches the cell image histogram to the MNIST
      dataset histogram.
    - The input cell_image is expected to be an RGB image with dimensions corresponding to a single
      Sudoku cell.
    """
     
    # Grayscale image
    cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

    # Smooth image
    cell_image = cv2.GaussianBlur(cell_image, (3, 3), 0)  

    # Remove outliers, could be caused by lighting effects
    # Calculate the percentiles and set limits 
    percentile_min = np.percentile(cell_image, 2)
    percentile_max = np.percentile(cell_image, 98)
    cell_image[cell_image < percentile_min] = percentile_min
    cell_image[cell_image > percentile_max] = percentile_max
  
    # Remove image background by thresholding
    otsu_threshold_value, _ = cv2.threshold(
        cell_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    cell_image = np.where(cell_image > otsu_threshold_value, 255, cell_image)

    # Inverse image
    cell_image = 255 - cell_image

    if is_filled(cell_image):
        cell_image = remove_border(cell_image)
        # Centre digit
        cell_image = centre_digit(cell_image)

        # Resize image
        cell_image = cv2.resize(cell_image, (28, 28))

        # Match histograms
        cell_image = match_histogram(cell_image)

        # Normalize in same technique as done on mnist 
        cell_image = (cell_image - np.min(cell_image)) / (np.max(cell_image) - np.min(cell_image)) 
        cell_image = (cell_image / np.max(cell_image) - 0.5) / 0.5  # Same normalisation as training

        return cell_image
    
    else:

        return None



def is_filled(cell_image):
    """
    Determine whether a Sudoku cell contains a digit.

    This function analyzes the central region of a Sudoku cell to decide if there is a digit present
    based on pixel intensity. It crops the image to the central 60% and compares the number of pixels
    above a certain threshold to a set ratio.

    Parameters:
    - cell_image (numpy.ndarray): A grayscale image of a Sudoku cell.

    Returns:
    - bool: True if a digit is detected in the cell, False otherwise.

    Notes:
    - The threshold value is set to 100, which is a chosen value for pixel intensity that
      represents a digit. This may need to be adjusted based on the image quality.
    - The function assumes that the presence of a significant number of bright pixels (above the
      threshold) indicates a digit.
    """
    height, width = cell_image.shape
    centre_region = cell_image[int(height*0.30):int(height*0.70), int(width*0.30):int(width*0.70)]

    threshold = 100
    digit_pixels = np.sum(centre_region > threshold)

    if digit_pixels > (0.1 * centre_region.size):
        return True
    else:
        return False



def remove_border(cell_image):
    """
    Remove any border from a Sudoku cell image while preserving the central digit.

    The function applies morphological operations to the input image to remove small objects and noise,
    which are often parts of the cell border. It then uses contour detection to identify and preserve
    the largest contour assumed to be the digit.

    Parameters:
    - cell_image (numpy.ndarray): A grayscale image of a Sudoku cell where the digit is brighter than
      the background.

    Returns:
    - numpy.ndarray: The processed image with the border removed, keeping only the largest contour.

    Notes:
    - A morphological opening operation with a 3x3 rectangular kernel is used to remove small objects.
    - The function assumes that the largest contour in the cell image after the morphological opening
      is the digit to be preserved.
    """

    # Use a kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Apply morphological opening to remove small objects like the line
    opening = cv2.morphologyEx(cell_image, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find contours on the opened image
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask where we will draw the kept contours (the digit)
    mask = np.zeros_like(cell_image)

    # Assume the largest contour is the digit and draw it on the mask
    # This is based on the assumption that the digit will be the largest object in the cell
    if contours:
        digit_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [digit_contour], -1, 255, -1)

    # Use the mask to keep only the digit in the original image
    result = cv2.bitwise_and(cell_image, cell_image, mask=mask)

    return result



def centre_digit(image):
    """
    Center a digit within an image using image moments to find the centroid.

    This function converts a grayscale image to a binary image and computes its moments to find the 
    centroid of the digit. It then calculates the necessary shift to center the digit within the image 
    and applies this transformation.

    Parameters:
    - image (numpy.ndarray): A grayscale image as a NumPy array with a digit to be centered.

    Returns:
    - numpy.ndarray: The image with the digit centered.

    Notes:
    - The image is first converted to a binary image using Otsu's thresholding method.
    - If the digit is already perfectly centered, or the centroid cannot be calculated, the original 
      image is returned unchanged.
    - The function assumes that the input image contains a single digit that needs to be centered.
    """
    # Convert to binary if the image is not already binary
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find the moments of the image to calculate the centroid
    M = cv2.moments(binary_image)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # Calculate the shift required to center the digit
    shiftX = image.shape[1] // 2 - cX
    shiftY = image.shape[0] // 2 - cY

    # Create a translation matrix and perform the shift
    M = np.float32([[1, 0, shiftX], [0, 1, shiftY]])
    centered_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return centered_image



def match_histogram(source, reference_hist_dir="mnist_average_histogram.npy"):
    """
    Adjust the pixel intensity distribution of a source image to match a reference histogram.

    This function matches the histogram of a source image to the histogram of a reference image or 
    a precomputed histogram array. This is often used to normalize lighting conditions between images 
    or to standardize image data before feeding it into a machine learning model.

    Parameters:
    - source (numpy.ndarray): Source image as a numpy array whose histogram is to be matched.
    - reference_hist_dir (str): Path to the .npy file containing the reference histogram.

    Returns:
    - numpy.ndarray: The source image with its histogram matched to the reference.

    Raises:
    - IOError: If the reference histogram file cannot be found.

    Notes:
    - The function assumes the source image is in grayscale.
    - The reference histogram is typically computed from a set of images (e.g., the MNIST dataset).
    - The matching is done based on the cumulative distribution function (CDF) of pixel intensities.
    """

     # Load MNIST histogram
    directory = os.path.dirname(os.path.abspath(__file__))
    mnist_hist_path = os.path.join(directory, reference_hist_dir)
        
    try:
        mnist_average_hist = np.load(mnist_hist_path)
    except IOError:
        raise IOError("Histogram file not found.")

    # Match histogramns
    reference_cdf = np.cumsum(mnist_average_hist)
    source = source / np.max(source)  # Histogram must be between 0 and 1 
    source_hist, bin_edges = np.histogram(source.flatten(), bins=256, range=[0, 256])
    source_cdf = np.cumsum(source_hist)

    mapping = np.interp(source_cdf, reference_cdf, bin_edges[:-1])
    matched = np.interp(source.flatten(), bin_edges[:-1], mapping)

    cell = matched.reshape(source.shape)

    return cell