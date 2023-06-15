from manim import *
import random


config.background_color = "#04f404"
textColor = "#000000"

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


class MiscQ(MovingCameraScene):
    def construct(self):
        q = Tex("?", color = WHITE).scale(6)
        map = ImageMobject("../maps/Laileia_noCityIcons.png").shift(RIGHT*4+DOWN*1).scale(0.38)

        smallQs = VGroup()
        for offset in offsets:
            smallQs.add(
                Tex("?", color = WHITE).shift(LEFT*offset[0]+UP*offset[1])
            )


        # self.add(map)
        self.wait(2)
        self.play(Write(q))
        self.wait(2)
        self.play(ReplacementTransform(q, smallQs))
        self.wait(2)
        self.play(FadeOut(smallQs))
        self.wait(2)
