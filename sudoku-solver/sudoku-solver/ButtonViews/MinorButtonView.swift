import SwiftUI

struct MinorButtonView: View {
    
    var text: String

    private let buttonWidth: CGFloat = 205
    private let buttonHeight: CGFloat = 39.12
    private let cornerRadius: CGFloat = 15
    private let strokeColor: Color = Color.black.opacity(0.70)
    private let shadowColor: Color = Color.black.opacity(0.25)
    private let backgroundColor: Color = Color(red: 0.67, green: 0.84, blue: 0.85)
    private let textColor: Color = Color(red: 0.95, green: 0.94, blue: 0.91)
    private let textStrokeColor: Color = Color.black
    private let textStrokeWidth: CGFloat = 1

    var body: some View {
        ZStack {
            Rectangle()
                .foregroundColor(.clear)
                .frame(width: buttonWidth, height: buttonHeight)
//                .background(backgroundColor)
                .background(Color(red: 0.98, green: 0.98, blue: 0.95))
                .cornerRadius(cornerRadius)
                .overlay(
                    RoundedRectangle(cornerRadius: cornerRadius)
                        .inset(by: 0.50)
                        .stroke(strokeColor, lineWidth: 0.50)
                )
                .shadow(color: shadowColor, radius: 4, y: 4)
            
            Text(text)
                .font(Font.custom("SF Pro Text", size: 18).weight(.bold))
                .foregroundColor(.black)
//                .foregroundColor(textColor)
//                .modifier(TextStrokeModifier(strokeWidth: textStrokeWidth, strokeColor: textStrokeColor))
        }
        .frame(width: buttonWidth, height: buttonHeight)
    }
}

struct MinorButtonView_Previews: PreviewProvider {
    static var previews: some View {
        MinorButtonView(text: "Sudoku Tips")
    }
}
