//
//  SudokuCell.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 11/01/2024.
//

import UIKit

final class SudokuCell: UIView {
    private var numberLabel: UILabel!
    var isEditable: Bool = false {
        didSet {
            numberLabel.isUserInteractionEnabled = isEditable
            updateAppearanceForEditability()
        }
    }
    var number: Int = 0 {
        didSet {
            numberLabel.text = number == 0 ? "" : "\(number)"
        }
    }

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupNumberLabel()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupNumberLabel()
    }

    private func setupNumberLabel() {
        numberLabel = UILabel()
        numberLabel.textAlignment = .center
        numberLabel.font = UIFont.systemFont(ofSize: 28)
        numberLabel.translatesAutoresizingMaskIntoConstraints = false
        self.addSubview(numberLabel)
        
        NSLayoutConstraint.activate([
            numberLabel.topAnchor.constraint(equalTo: self.topAnchor),
            numberLabel.bottomAnchor.constraint(equalTo: self.bottomAnchor),
            numberLabel.leadingAnchor.constraint(equalTo: self.leadingAnchor),
            numberLabel.trailingAnchor.constraint(equalTo: self.trailingAnchor)
        ])
        
        let tapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(handleTap))
        numberLabel.isUserInteractionEnabled = true // Make sure the label can receive taps
        numberLabel.addGestureRecognizer(tapGestureRecognizer)
    }
    
    // Handler for tap gestures
    @objc private func handleTap() {
        guard isEditable else { return }
        // Notify a delegate or use a closure to inform the SudokuGridView that a cell was tapped
    }
    
    func updateAppearanceForEditability() {
           // Change the appearance based on the editability
           // For example, changing the background color slightly or adding a border
           self.backgroundColor = isEditable ? UIColor.lightGray : UIColor.white
       }
    
}
