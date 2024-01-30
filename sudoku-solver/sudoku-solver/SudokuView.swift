//
//  SudokuView.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 11/01/2024.
//

import SwiftUI


struct SudokuView: View {
    
    @State var exampleSudokuData: [[Int]] = [
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
    @State private var isEditable: Bool = false
    
    var body: some View {
        ZStack {
            Rectangle()
                .foregroundColor(Color(red: 0.61, green: 0.72, blue: 0.8))
                .ignoresSafeArea()
            VStack {
                Spacer()
                Image("app_logo_2")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 50)
                Text("SUDOKU HELPER")
                  .font(
                    Font.custom("SF Pro Rounded", size: 36)
                      .weight(.black)
                  )
                  .foregroundColor(Color(red: 0.95, green: 0.94, blue: 0.91))
                  .modifier(TextStrokeModifier(strokeWidth: 1, strokeColor: .black))
                
                Spacer()
                
//                SudokuGridViewRepresentable(numbers: exampleSudokuData)
//                    .frame(width: UIScreen.main.bounds.width * 0.95, height: UIScreen.main.bounds.width * 0.95)
//                    .previewLayout(.sizeThatFits)
//                    .cornerRadius(10)
                SudokuGridViewRepresentable(numbers: exampleSudokuData, isEditable: isEditable)
                    .frame(width: UIScreen.main.bounds.width * 0.95, height: UIScreen.main.bounds.width * 0.95)
                    .previewLayout(.sizeThatFits)
                    .cornerRadius(10)
                
       
                Spacer()
                    
                
                Text("Did We Get It Right?")
                  .font(
                    Font.custom("SF Pro Rounded", size: 30)
                      .weight(.black)
                  )
                  .foregroundColor(Color(red: 0.95, green: 0.94, blue: 0.91))
                  .modifier(TextStrokeModifier(strokeWidth: 1, strokeColor: .black))
                
                
                Button(action: {
                    let solver = SudokuSolver()
                    if solver.solve(&exampleSudokuData) {
                        print("Sudoku solved!")
                    } else {
                        print("No solution exists.")
                    }
                }, label: {
                    MinorButtonView(text: "Yes, Begin Solving")
                })

                
                
                
                // Toggle editability button
                Button(action: {
                    self.isEditable.toggle()
                }) {
                    MinorButtonView(text: "No, Edit Sudoku")
                }
                
                
                
                Spacer()


            }
                
        }
    
    }
}

#Preview {
    SudokuView()
}
