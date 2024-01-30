//
//  SudokuGridView.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 11/01/2024.
//


// SudokuGridView.swift

// SudokuGridView.swift


import UIKit


protocol SudokuGridViewDelegate: AnyObject {
    func cellTapped(_ cell: SudokuCell, atRow row: Int, column: Int)
}

final class SudokuGridView: UIView {
    weak var delegate: SudokuGridViewDelegate?
    var cells = [[SudokuCell]]()
    private let subGridLineWidth: CGFloat = 4
    private let cellLineWidth: CGFloat = 1
    private let gridColor: UIColor = .black
    

    // Initialization
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.backgroundColor = .init(red: 0.98, green: 0.98, blue: 0.95, alpha: 1)
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        self.backgroundColor = .white
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()

        // Set the border color, width, and corner radius
        layer.borderColor = UIColor.black.cgColor
        layer.borderWidth = 2 // You can change this value to your desired border thickness
        layer.cornerRadius = 8 // Optional: if you want rounded corners
    }

    // Function to initialize the Sudoku grid with a 2D array
    func initializeGrid(with numbers: [[Int]]) {
        guard numbers.count == 9 && numbers.allSatisfy({ $0.count == 9 }) else { return }
        
        cells.forEach { row in row.forEach { $0.removeFromSuperview() } }
        cells.removeAll()
        
        for (rowIndex, row) in numbers.enumerated() {
            var cellRow = [SudokuCell]()
            for (columnIndex, number) in row.enumerated() {
                let cell = SudokuCell()
                cell.number = number
                cell.translatesAutoresizingMaskIntoConstraints = false
                self.addSubview(cell)
                cellRow.append(cell)
            }
            cells.append(cellRow)
        }
        setNeedsUpdateConstraints()
    }

    // This method is called when the constraints need to be updated
    override func updateConstraints() {
        super.updateConstraints()
        setupCellsConstraints()
    }

    // Set up constraints for the cells
    private func setupCellsConstraints() {
        let cellSize = (bounds.width - (subGridLineWidth * 2 + cellLineWidth * 6)) / 9
        for rowIndex in 0..<9 {
            for columnIndex in 0..<9 {
                let cell = cells[rowIndex][columnIndex]
                NSLayoutConstraint.activate([
                    cell.topAnchor.constraint(equalTo: topAnchor, constant: CGFloat(rowIndex / 3) * subGridLineWidth + CGFloat(rowIndex) * cellLineWidth + CGFloat(rowIndex) * cellSize),
                    cell.leadingAnchor.constraint(equalTo: leadingAnchor, constant: CGFloat(columnIndex / 3) * subGridLineWidth + CGFloat(columnIndex) * cellLineWidth + CGFloat(columnIndex) * cellSize),
                    cell.widthAnchor.constraint(equalToConstant: cellSize),
                    cell.heightAnchor.constraint(equalToConstant: cellSize)
                ])
            }
        }
    }

    // Draw method for custom drawing
    override func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }

        // Draw thick lines for subgrid borders
        context.setLineWidth(subGridLineWidth)
        gridColor.set()
        drawSubGridBorders(with: context, in: rect)
        
        // Draw thin lines for cell borders
        context.setLineWidth(cellLineWidth)
        drawCellBorders(with: context, in: rect)
    }

    // Draws subgrid borders
    private func drawSubGridBorders(with context: CGContext, in rect: CGRect) {
        let fullGridSize = rect.width
        let subGridSize = fullGridSize / 3

        for i in 1...2 {
            let lineOffset = subGridSize * CGFloat(i)
            // Vertical lines
            context.move(to: CGPoint(x: lineOffset, y: 0))
            context.addLine(to: CGPoint(x: lineOffset, y: fullGridSize))
            
            // Horizontal lines
            context.move(to: CGPoint(x: 0, y: lineOffset))
            context.addLine(to: CGPoint(x: fullGridSize, y: lineOffset))
        }
        context.strokePath()
    }

    // Draws cell borders
    private func drawCellBorders(with context: CGContext, in rect: CGRect) {
        let fullGridSize = rect.width
        let cellSize = fullGridSize / 9
        
        for i in 1...8 {
            if i % 3 == 0 { continue } // Skip subgrid borders
            
            let lineOffset = cellSize * CGFloat(i)
            // Vertical lines
            context.move(to: CGPoint(x: lineOffset, y: 0))
            context.addLine(to: CGPoint(x: lineOffset, y: fullGridSize))
            
            // Horizontal lines
            context.move(to: CGPoint(x: 0, y: lineOffset))
            context.addLine(to: CGPoint(x: fullGridSize, y: lineOffset))
        }
        context.strokePath()
    }
    
//    // Make editable
//    func setGridEditable(_ isEditable: Bool) {
//        cells.forEach { row in
//            row.forEach { cell in
//                cell.isEditable = isEditable
//            }
//        }
//    }

}
