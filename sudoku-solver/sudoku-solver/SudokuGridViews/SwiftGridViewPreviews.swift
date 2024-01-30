//
//  SwiftGridViewPreviews.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 11/01/2024.
//
import SwiftUI

// SwiftUI wrapper for your SudokuGridView
struct SudokuGridViewRepresentable: UIViewRepresentable {
    var numbers: [[Int]]
    var isEditable: Bool

    // Create the UIView instance to be presented by SwiftUI
    func makeUIView(context: Context) -> SudokuGridView {
        let gridView = SudokuGridView()
        gridView.initializeGrid(with: numbers)
        return gridView
    }

    // Update the view with new data if needed
    func updateUIView(_ uiView: SudokuGridView, context: Context) {
        // Update the grid if your numbers array changes
        uiView.initializeGrid(with: numbers)
//        uiView.setGridEditable(isEditable)
    }
}

// Preview provider for SwiftUI previews
struct SudokuGridView_Previews: PreviewProvider {
    static var previews: some View {
        // Initialize with an example Sudoku data array
        let exampleSudokuData: [[Int]] = [
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
        
        SudokuGridViewRepresentable(numbers: exampleSudokuData, isEditable: true)
            .frame(width: UIScreen.main.bounds.width * 0.95, height: UIScreen.main.bounds.width * 0.95)
            .previewLayout(.sizeThatFits)
    }
}
