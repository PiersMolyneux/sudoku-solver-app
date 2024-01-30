//
//  SudokuViewController.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 11/01/2024.
//

import UIKit

// Ensure that your view controller conforms to the SudokuGridViewDelegate protocol
class SudokuViewController: UIViewController, SudokuGridViewDelegate {
    private var sudokuGridView: SudokuGridView!
    private var editToggle: UISwitch!

    private var enableEditButton: UIButton!
    private var disableEditButton: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupSudokuGridView()
        setupEditToggle()
        setupEditButtons()
    }

    private func setupEditButtons() {
        // Setup Enable Edit Button
        enableEditButton = UIButton(type: .system)
        enableEditButton.setTitle("Enable Edit", for: .normal)
        enableEditButton.addTarget(self, action: #selector(enableEditMode), for: .touchUpInside)
        enableEditButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(enableEditButton)

        // Setup Disable Edit Button
        disableEditButton = UIButton(type: .system)
        disableEditButton.setTitle("Disable Edit", for: .normal)
        disableEditButton.addTarget(self, action: #selector(disableEditMode), for: .touchUpInside)
        disableEditButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(disableEditButton)

        // Set constraints for the buttons
        // Adjust the constraints as per your layout
        NSLayoutConstraint.activate([
            enableEditButton.topAnchor.constraint(equalTo: editToggle.bottomAnchor, constant: 20),
            enableEditButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            disableEditButton.topAnchor.constraint(equalTo: enableEditButton.bottomAnchor, constant: 10),
            disableEditButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }

    @objc private func enableEditMode() {
        editToggle.setOn(true, animated: true)
        toggleEditing()
    }

    @objc private func disableEditMode() {
        editToggle.setOn(false, animated: true)
        toggleEditing()
    }

    private func setupSudokuGridView() {
        sudokuGridView = SudokuGridView()
        sudokuGridView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(sudokuGridView)
        
        // Set the delegate to the view controller
        sudokuGridView.delegate = self

        // Set constraints for the grid view
        NSLayoutConstraint.activate([
            sudokuGridView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            sudokuGridView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            sudokuGridView.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.95),
            sudokuGridView.heightAnchor.constraint(equalTo: sudokuGridView.widthAnchor)
        ])

        // Initialize the grid with a starting puzzle
        let startingPuzzle: [[Int]] = [
            // ... A 9x9 array representing the initial puzzle
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        sudokuGridView.initializeGrid(with: startingPuzzle)
    }

    private func setupEditToggle() {
        editToggle = UISwitch()
        editToggle.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(editToggle)
        
        NSLayoutConstraint.activate([
            editToggle.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),
            editToggle.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -20)
        ])

        editToggle.addTarget(self, action: #selector(toggleEditing), for: .valueChanged)
    }

    @objc private func toggleEditing() {
        // When the toggle changes, update each cell's isEditable property
        let isEditable = editToggle.isOn
        sudokuGridView.cells.forEach { row in
            row.forEach { cell in
                cell.isEditable = isEditable
                cell.updateAppearanceForEditability()
            }
        }
    }
    
    // SudokuGridViewDelegate method
    func cellTapped(_ cell: SudokuCell, atRow row: Int, column: Int) {
        // Check if the cell is editable before allowing the user to make changes
        guard cell.isEditable else { return }
        
        let alertController = UIAlertController(title: "Edit Cell", message: "Enter a number", preferredStyle: .alert)
        alertController.addTextField { textField in
            textField.keyboardType = .numberPad
            textField.text = cell.number == 0 ? "" : String(cell.number)
        }
        let confirmAction = UIAlertAction(title: "OK", style: .default) { [weak alertController, weak self] _ in
            if let textField = alertController?.textFields?.first, let text = textField.text, let number = Int(text) {
                // Make sure the number is between 1 and 9
                if number >= 1 && number <= 9 {
                    // Update the cell's number
                    cell.number = number
                    // Optionally, update your data model here
                } else {
                    // Handle the error, perhaps clear the cell if the number is not valid
                    cell.number = 0
                }
            }
        }
        let cancelAction = UIAlertAction(title: "Cancel", style: .cancel, handler: nil)
        alertController.addAction(confirmAction)
        alertController.addAction(cancelAction)
        
        present(alertController, animated: true, completion: nil)
    }
}
