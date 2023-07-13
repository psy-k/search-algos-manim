from  manim import *

class PathKey:
    def __init__(self, color, title, offset):
        self.color = color
        self.title = title
        self.offset = offset
        
        leftDot = Dot(radius=0.05, stroke_width=0, fill_color = color)       
        rightDot = Dot(radius=0.05, stroke_width=0, fill_color = color).shift(RIGHT*0.2)

        # if dashed == True:
        line = DashedLine(
            start=leftDot.get_center(), 
            end=rightDot.get_center(), 
            color =color, stroke_width = 2.5,
            dash_length=0.5, dashed_ratio=0.9
        ) 
        # else:
        #     line = Line(
        #         start=leftDot.get_center(), 
        #         end=rightDot.get_center(), 
        #         color =color, stroke_width = 2.5
        #     )     

        keyVisual = VGroup(leftDot, rightDot, line)
        keyText = Tex(title, color=BLACK).scale(0.3).next_to(rightDot, RIGHT).shift(LEFT*0.1)
        key = VGroup(
            # leftDot, rightDot, 
            line, keyText)

        key.shift(offset)

        self.keyVisual = keyVisual
        self.keyText = keyText
        self.key = key


