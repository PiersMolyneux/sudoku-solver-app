// TextStrokeModifier.swift

import SwiftUI

struct TextStrokeModifier: ViewModifier {
    var strokeWidth: CGFloat
    var strokeColor: Color
    var fillColor: Color = .white

    func body(content: Content) -> some View {
        content
            .overlay(
                content
                    .foregroundColor(fillColor)
            )
            .foregroundColor(strokeColor)
            .shadow(color: strokeColor, radius: strokeWidth)
    }
}
