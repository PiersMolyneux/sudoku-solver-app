//
//  SudokuSolver.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 25/01/2024.
//

import Foundation

class SudokuSolver {

    // Main function to solve Sudoku
    func solve(_ sudoku: inout [[Int]]) -> Bool {
        guard let emptyCell = findNextEmptyCell(sudoku) else {
            return true  // Sudoku solved
        }

        let (row, col) = emptyCell

        for value in 1...9 {
            if isValidPlacement(sudoku, row: row, col: col, value: value) {
                sudoku[row][col] = value
                if solve(&sudoku) {
                    return true
                }
                sudoku[row][col] = 0  // Backtrack
            }
        }

        return false  // Backtrack if no valid number found
    }

    // Find the next empty cell in the Sudoku grid
    private func findNextEmptyCell(_ sudoku: [[Int]]) -> (Int, Int)? {
        for row in 0..<9 {
            for col in 0..<9 {
                if sudoku[row][col] == 0 {
                    return (row, col)
                }
            }
        }
        return nil
    }

    // Check if placing a value in a specified cell is valid
    private func isValidPlacement(_ sudoku: [[Int]], row: Int, col: Int, value: Int) -> Bool {
        // Check row and column
        for i in 0..<9 {
            if sudoku[row][i] == value || sudoku[i][col] == value {
                return false
            }
        }

        // Check 3x3 subgrid
        let startRow = 3 * (row / 3)
        let startCol = 3 * (col / 3)
        for i in startRow..<startRow+3 {
            for j in startCol..<startCol+3 {
                if sudoku[i][j] == value {
                    return false
                }
            }
        }

        return true
    }
}
