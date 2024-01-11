
# Sudoku Solver App

## Overview
The Sudoku Solver app is an iPhone application designed to effortlessly solve Sudoku puzzles using  image recognition and puzzle-solving algorithms. With the convenience of a snapshot, users can capture any Sudoku puzzle, and the app swiftly processes and presents the solution or gives the user a next-step hint. The backend is powered by Python, utilizing OpenCV and PyTorch for  image processing and algorithmic resolution. The frontend, developed in Swift, ensures a fluid and user-friendly experience, integrating with the backend capabilities.

### Note to Users and Developers
My journey in developing this app included learning Swift for the frontend implementation. While my expertise is more pronounced in backend development, the frontend aspects of the app were created with equal dedication. However, as I am relatively new to frontend development and app design, there may be areas for improvement or overlooked efficiencies. I am open to feedback and suggestions for both the backend and frontend components of the app. If you have any insights or notice any potential enhancements, please feel free to reach out to me at piersmolyd@gmail.com. 


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
    - **app.py**: Main Python script creating api.
    - **services/**: Supporting services for `script.py`.
      - **image_processing/**: Modules for processing Sudoku images.
        - **loader.py**: Loads Sudoku pictures.
        - **image_preprocessor.py**: Preprocesses Sudoku photo to be used.
        - **cell_preprocessor.py**: Preprocesses Sudoku cells to be inputted into model.
        - **cell_configurator.py**: Extra cell specific functions unrelated to image preprocessing.
        - **mnist_average_histogram.npy**: Used for histogram matching of inputs to mnist.
        - **digit_recognition/**: Machine Learning model for individual cell digit recognition.
          - **model.py**: The ML model definition.
          - **trainmodel.py**: Script for training the model.
          - **tools.py**: Utilities for preparing cells for model predictions.
      - **solver/**: Sudoku solving logic.
        - **sudoku_solver.py**: Solves Sudoku represented as a numpy array.
  - **data/**: Examples used for testing the backend.
    - **sudoku_tests/**: Sudoku images for testing code functionality.

- **sudoku-solver/**: Frontend for the app
  - **sudoku-solver.xcodeproj**: Frontend app file
  - **sudoku-solver/**: Supporting files for frontend
  

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

