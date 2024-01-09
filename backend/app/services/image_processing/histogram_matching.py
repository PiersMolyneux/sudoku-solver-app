import numpy as np
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import os



def calculate_average_histogram(mnist_dataset):
    """
    Calculate the average histogram of the MNIST dataset.

    Parameters:
    - mnist_dataset: Dataset object from torchvision.datasets.

    Returns:
    - average_hist: Average histogram as a numpy array.
    """
    hist_sum = np.zeros(256)
    to_tensor = transforms.ToTensor()  # Transform to convert PIL Image to PyTorch tensor

    # Iterate through the MNIST dataset
    for image, _ in mnist_dataset:
        # Convert PIL Image to tensor, then to numpy array
        image_tensor = to_tensor(image)
        hist, _ = np.histogram(image_tensor.numpy().flatten(), bins=256, range=[0, 1])
        hist_sum += hist

    # Calculate the average histogram
    average_hist = hist_sum / len(mnist_dataset)
    return average_hist

def save_histogram(histogram, filename):
    """
    Save a histogram to a file.

    Parameters:
    - histogram: Histogram array to be saved.
    - filename: Name of the file to save the histogram.
    """
    np.save(filename, histogram)

def load_histogram(filename):
    """
    Load a histogram from a file.

    Parameters:
    - filename: Name of the file to load the histogram from.

    Returns:
    - Loaded histogram as a numpy array.
    """
    try:
        return np.load(filename)
    except IOError:
        raise IOError("Histogram file not found.")


# Main script execution
if __name__ == "__main__":
    mnist_train = datasets.MNIST(root='./data', train=True, download=True, transform=None)
    average_hist = calculate_average_histogram(mnist_train)
    save_histogram(average_hist, 'mnist_average_histogram.npy')
