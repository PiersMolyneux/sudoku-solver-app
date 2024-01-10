// MajorButtonView.swift

import SwiftUI

struct MajorButtonView: View {
    var text: String

    var body: some View {
        ZStack {
            Rectangle()
                .foregroundColor(Color(red: 0.98, green: 0.98, blue: 0.95))
//                .foregroundColor(.clear)
                .frame(width: 300, height: 54)
                .background(Color(red: 0.57, green: 0.78, blue: 0.81))
                .cornerRadius(15)
                .overlay(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color.black.opacity(0.70), lineWidth: 0.50)
                )
                .shadow(color: Color.black.opacity(0.25), radius: 4, y: 4)

            Text(text)
                .font(Font.custom("SFProText-Bold", size: 22))
//                .foregroundColor(Color(red: 0.95, green: 0.94, blue: 0.91))
                .foregroundStyle(.black)
                .modifier(TextStrokeModifier(strokeWidth: 1, strokeColor: .white))
        }
        .frame(width: 300, height: 54)
    }
}

struct MajorButtonView_Previews: PreviewProvider {
    static var previews: some View {
        MajorButtonView(text: "Upload File")
    }
}
