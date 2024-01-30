from flask import Flask, request, jsonify
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from script import process_image, solve  # Assuming script.py is in the same directory

app = Flask(__name__)

def allowed_file(filename):
    """
    Check if the file extension is allowed.

    Parameters:
    filename (str): The name of the file.

    Returns:
    bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

def read_image(file):
    """
    Read an image file and convert it to a numpy array.

    Parameters:
    file (FileStorage): The image file uploaded by the user.

    Returns:
    numpy.ndarray: The image in numpy array format.
    """
    in_memory_file = file.read()
    nparr = np.frombuffer(in_memory_file, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


@app.route('/upload', methods=['POST'])
def process_sudoku():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "No selected file or invalid file format"}), 400

    try:
        img = read_image(file)
        sudoku_grid = process_image(img)
        grid_list = sudoku_grid.tolist()
        return jsonify({"sudokuGrid": grid_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    if not data or 'sudokuGrid' not in data:
        return jsonify({"error": "No sudoku grid provided"}), 400

    sudoku_grid = np.array(data['sudokuGrid'])
    
    try:
        solved_sudoku = solve(sudoku_grid)
        solved_sudoku_list = solved_sudoku.tolist()
        return jsonify({"solvedSudoku": solved_sudoku_list}), 200
    except ValueError:
        return jsonify({"error": "Could not solve sudoku"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
