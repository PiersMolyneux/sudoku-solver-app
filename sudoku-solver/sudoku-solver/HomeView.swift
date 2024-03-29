//
//  HomeView.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 09/01/2024.
//

import SwiftUI

struct HomeView: View {
    var body: some View {
        
        NavigationView {
            
            ZStack {
                Rectangle()
                    .foregroundColor(Color(red: 0.61, green: 0.72, blue: 0.8))
                    .background(Color(red: 0.61, green: 0.72, blue: 0.8))
                VStack {
                    Spacer()
                    Image("app_logo_2")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 260)
                        .padding()
                    
                    Text("SUDOKU HELPER")
                        .font(
                            Font.custom("SF Pro Rounded", size: 36)
                                .weight(.black)
                        )
                        .foregroundColor(Color(red: 0.95, green: 0.94, blue: 0.91))
                        .modifier(TextStrokeModifier(strokeWidth: 1, strokeColor: .black))
                        .padding()
                    
                    // Now for buttons
                    NavigationLink(destination: SudokuView()) {
                        MajorButtonView(text: "Upload Sudoku")
                            .padding()
                    }
                    
                    NavigationLink(destination: SudokuTipsView()) {
                        MinorButtonView(text: "Sudoku Tips")
                    }

                    MinorButtonView(text: "Info")
                    Spacer()
//                    Spacer()
                }
            }
        }
        .ignoresSafeArea()
        
        
        
    }
}

#Preview {
    HomeView()
}
