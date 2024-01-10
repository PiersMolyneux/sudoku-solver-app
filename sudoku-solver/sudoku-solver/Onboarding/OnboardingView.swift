//
//  OnboardingView.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 10/01/2024.
//


import SwiftUI

struct OnboardingView: View {
    
//    @Environment(BusinessModel.self) var model
    @Environment(\.dismiss) var dismiss
    @State var selectedViewIndex = 0
    
    var body: some View {
        ZStack {
            if selectedViewIndex == 0 {
                Color(red: 111/255, green: 154/255, blue: 189/255)
            }
            else {
                Color(red: 139/255, green: 166/255, blue: 65/255)
            }
            TabView(selection: $selectedViewIndex) {
                OnboardingViewDetails(bgColor: Color(red: 111/255, green: 154/255, blue: 189/255), headline: "Welcome to your Sudoku Helper", subHeadline: "We can help you with those tricky sudokus!") {
                    withAnimation {
                        selectedViewIndex = 1
                    }
                }
                .tag(0)
                .ignoresSafeArea()
                
                OnboardingViewDetails(bgColor: Color(red: 139/255, green: 166/255, blue: 200/255), headline: "Just upload a photo!", subHeadline: "We'll do the rest, giving you the opportunity to either unveal a hidden square, or solve the whole thing!") {
//                    model.getUserLocation()
                    dismiss()
                }
                .tag(1)
                .ignoresSafeArea()

            }
            .tabViewStyle(.page(indexDisplayMode: .never))
            
            VStack {
                Spacer() // push to bottm
                HStack (spacing: 16) {
                    Spacer()
                    Circle()
                        .frame(width: 10)
                        .foregroundStyle(selectedViewIndex == 0 ? .white : .gray)
                    Circle()
                        .frame(width: 10)
                        .foregroundStyle(selectedViewIndex == 1 ? .white : .gray)
                    Spacer()
                }
                .padding(.bottom, 190)

            }
        }
        .ignoresSafeArea()
    }
}

#Preview {
    OnboardingView()
}
