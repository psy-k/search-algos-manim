from manim import *
import random


config.background_color = "#04f404"
# config.background_color = "#ffffff"
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


class MiscDot(MovingCameraScene):
    def construct(self):

        dot = Dot( color = targetCityIconCenterColor, stroke_color = targetCityIconBorderColor, radius=0.2, stroke_width= 4)

        self.add(dot)
        