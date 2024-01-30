//
//  SudokuTipsView.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 25/01/2024.
//

import SwiftUI

struct SudokuTipsView: View {
    let tipsText = """
    Here are some Sudoku tips to help you solve these popular number puzzles:
    
    1. Start with the Easy Numbers:
       Begin by identifying and filling in any obvious numbers that are already given in the puzzle. Look for rows, columns, or 3x3 boxes with a lot of pre-filled numbers and use those as starting points.
    
    2. Look for Unique Possibilities:
       Examine each row, column, and 3x3 box to find cells where only one number can fit based on the numbers already placed in that row, column, or box. This is often referred to as "elimination."
    
    3. Scan for Twins and Triplets:
       Search for pairs or triples of the same number in rows, columns, or boxes. If two cells in a row, column, or box can only contain the same two numbers, you can eliminate those numbers from other cells in the same row, column, or box.
    
    4. Use Pencil Marks:
       In each cell, lightly pencil in the possible numbers that could go there based on the existing numbers in the row, column, and box. This can help you visualize possibilities and spot patterns.
    
    5. Focus on Empty Rows and Columns:
       If you find an empty row or column within a 3x3 box, try to fill it in. Similarly, if you have an empty 3x3 box within a row or column, try to fill that in as well.
    
    6. Practice Systematic Trial and Error:
       If you can't make further progress using the above techniques, it's okay to try placing a number in a cell and see if it leads to any contradictions. If it does, you can backtrack and try a different number. This is a form of logical deduction known as "trial and error."
    
    7. Look for Hidden Singles:
       Sometimes, a cell may only have one possible number left, but it's not immediately obvious. Carefully check rows, columns, and boxes to find these hidden singles.
    
    8. Maintain Consistency:
       Ensure that your placements adhere to the rules of Sudoku. Each row, column, and 3x3 box must contain all the numbers from 1 to 9 without repetition.
    
    9. Keep an Eye on Patterns:
       As you gain experience, you'll start recognizing common patterns and techniques that can help you solve more complex Sudoku puzzles. Some examples include X-Wings, Swordfish, and Jellyfish.
    
    10. Practice, Practice, Practice:
        The more you practice solving Sudoku puzzles, the better you'll become at recognizing strategies and spotting patterns. Start with easy puzzles and gradually work your way up to harder ones.
    
    Remember that Sudoku is a game of logic and deduction, so patience and practice are key to improving your skills. Enjoy the challenge and have fun!
    """
    
    var body: some View {
        
        ZStack{
            Rectangle()
                .foregroundColor(Color(red: 0.61, green: 0.72, blue: 0.8))
                .background(Color(red: 0.61, green: 0.72, blue: 0.8))
                .ignoresSafeArea()
            
            
            
            ScrollView {
                
                Text(tipsText)
                    .font(Font.custom("SFProText-Bold", size: 22))
                //                    .font(.body)
                    .padding()
                    .foregroundStyle(.black)
                    .modifier(TextStrokeModifier(strokeWidth: 0.1, strokeColor: .white))
            }
        }
        .navigationBarTitle("Sudoku Tips")
        
        
    }
}

struct SudokuTipsView_Previews: PreviewProvider {
    static var previews: some View {
        SudokuTipsView()
    }
}
