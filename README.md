# sudoku-solver-app

## Overview
This Sudoku Solver app is an innovative iPhone application that uses advanced image recognition and solving algorithms to solve Sudoku puzzles. Users can simply take a picture of a Sudoku puzzle, and the app will display the solved puzzle. The app leverages a Python backend with OpenCV and PyTorch for image processing and puzzle solving, and a Swift-based frontend for a seamless user experience.

## Features
- **Image Recognition**: Employs a robust CNN algorithm to recognize the puzzle digits.
- **Image Handling**: Utilizes OpenCV for image handling
- **Puzzle Solving**: A robust recursive programming technique is used to solve the puzzle.
- **Intuitive Interface**: A user-friendly Swift-based frontend for easy interaction with the app.

## Installation
Todo:

## Usage
Todo:

## Folder and File Structure

The `sudoku-solver-app` project is structured as follows:

- **backend/**: Contains all backend-related code.
  - **app/**: Main application scripts and services.
    - **script.py**: Main Python script for solving Sudoku from an image.
    - **services/**: Supporting services for `script.py`.
      - **image_processing/**: Modules for processing Sudoku images.
        - **loader.py**: Loads Sudoku pictures.
        - **preprocessor.py**: Preprocesses Sudoku images for model prediction.
        - **cell_configurator.py**: Prepares individual Sudoku cells for model prediction.
        - **digit_recognition/**: Machine Learning model for individual cell digit recognition.
          - **model.py**: The ML model definition.
          - **trainmodel.py**: Script for training the model.
          - **tools.py**: Utilities for preparing cells for model predictions.
          - **data/MNIST/**: MNIST dataset for model training.
      - **solver/**: Sudoku solving logic.
        - **sudoku_solver.py**: Solves Sudoku represented as a numpy array.
  - **data/**: Data used by the backend.
    - **sudoku_tests/**: Sudoku images for testing code functionality.

- **frontend/**: 


## Contributing
Guidelines for those who wish to contribute to the project.

## License
This project is licensed under the MIT License.

## Contact
Contact me at piersmoly@gmail.com if you have any questions

## Acknowledgements
Todo:

## Additional Resources
Todo:

