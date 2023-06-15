from manim import *
import random


config.background_color = "#04f404"
textColor = "#000000"

discoveredCityIconCenterColor = "#c7cbbb"
discoveredCityIconBorderColor= "#7e8a87"

visitedCityIconCenterColor = "#f6edd5"
visitedCityIconBorderColor = "#72472c"

targetCityIconCenterColor = "#ffefaf"
targetCityIconBorderColor = "#ffce00"

dashedEdgeColor = "#b02222"
dashedEdgeColorGreyed = "#7e8a87"
dotRadius = 0.05


offsets =[
    [0,0],
    [1.8,0.9],
    [-1.1,-0.8],
    [-0.6,1],
    [1.6,-1.8],
    [0.3,2.2],
    [3.2,-0.8],
    [1.3,-0.4],
    [3.3,-2.4],
]


class MiscFadeIn(MovingCameraScene):
    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png").shift(RIGHT*5+UP*1).scale(0.7)
        mapPin = ImageMobject("../maps/mapPin.png").scale(0.015)

        a = Dot(
                radius=dotRadius, 
                point=LEFT*1+UP*0.9, 
                color=discoveredCityIconCenterColor, 
                stroke_width=1.5, 
                stroke_color=discoveredCityIconBorderColor
            ).scale(2)

        b = Dot(
                radius=dotRadius, 
                point=LEFT*0+DOWN*1.9, 
                color=discoveredCityIconCenterColor, 
                stroke_width=1.5, 
                stroke_color=discoveredCityIconBorderColor
            ).scale(2)

        c = Dot(
                radius=dotRadius, 
                point=RIGHT*2+DOWN*0.3, 
                color=discoveredCityIconCenterColor, 
                stroke_width=1.5, 
                stroke_color=discoveredCityIconBorderColor
            ).scale(2)
        

        dashedToAGrey = DashedLine(
                        a.get_center()+(LEFT*2+UP*4), 
                        a.get_center(), 
                        color=dashedEdgeColorGreyed,
                        stroke_width = 2,
                        dash_length= 0.13
                    )

        dashedToATravelled = DashedLine(
                        a.get_center()+(LEFT*2+UP*4), 
                        a.get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 2,
                        dash_length= 0.13
                    )
        

        dashedToABGrey = DashedLine(
                        a.get_center(), 
                        b.get_center(), 
                        color=dashedEdgeColorGreyed,
                        stroke_width = 2,
                        dash_length= 0.13
                    )

        dashedToABTravelled = DashedLine(
                        a.get_center(), 
                        b.get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 2,
                        dash_length= 0.13
                    )
        

        dashedToACGrey = DashedLine(
                        a.get_center(), 
                        c.get_center(), 
                        color=dashedEdgeColorGreyed,
                        stroke_width = 2,
                        dash_length= 0.13
                    )

        dashedToACTravelled = DashedLine(
                        a.get_center(), 
                        c.get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 2,
                        dash_length= 0.13
                    )
        
        a.set_z_index(dashedToAGrey.z_index+1)
        a.set_z_index(dashedToATravelled.z_index+1)
        
        a.set_z_index(dashedToABGrey.z_index+1)
        b.set_z_index(dashedToABGrey.z_index+1)
        a.set_z_index(dashedToABTravelled.z_index+1)
        b.set_z_index(dashedToABTravelled.z_index+1)
        
        a.set_z_index(dashedToACGrey.z_index+1)
        c.set_z_index(dashedToACGrey.z_index+1)
        a.set_z_index(dashedToACTravelled.z_index+1)
        c.set_z_index(dashedToACTravelled.z_index+1)
        mapPin.set_z_index(a.z_index+1).move_to(a.get_center()+(LEFT*2+UP*4)+UP*0.15)

        A = Tex("A", color=BLACK).next_to(a, LEFT).scale(0.45).shift(RIGHT*0.2)
        B = Tex("B", color=BLACK).next_to(b, LEFT).scale(0.45).shift(RIGHT*0.2)
        C = Tex("C", color=BLACK).next_to(c, DOWN).scale(0.45).shift(UP*0.2)


        self.camera.frame.scale(0.7).shift(RIGHT*1+UP*0.2)
        self.add(map, a, dashedToAGrey, mapPin, A )

        self.wait()
        self.play(LaggedStart(mapPin.animate.move_to(a.get_center()+UP*0.15), Create(dashedToATravelled),lag_ratio=0.15))
        self.play(a.animate.set_fill_color(visitedCityIconCenterColor), FadeIn(B, C, b, c, dashedToABGrey, dashedToACGrey))
        self.wait(2)