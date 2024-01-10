//
//  sudoku_solverApp.swift
//  sudoku-solver
//
//  Created by Molyneux, Piers on 09/01/2024.
//

import SwiftUI

@main
struct sudoku_solverApp: App {
    @AppStorage("onboarding") var needsOnboarding = true
    var body: some Scene {
        WindowGroup {
            HomeView()
                .fullScreenCover(isPresented: $needsOnboarding) {
                    needsOnboarding = false
                } content: {
                    OnboardingView()
                         // needs to pass business model to onboarding view so we can request permission
                }
        }
    }
}
