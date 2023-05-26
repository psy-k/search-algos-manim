from manim import *

colorCityIconCenter = "#f6edd5"
colorCityIconBorder = "#72472c"
dotRadius = 0.05

color1 = RED
color2 = BLUE
color3 = GREEN
color4 = PINK


class City:
    def __init__(self, name, adjList, adjListDist, mobject):
        self.name = name
        self.adjList = adjList
        self.adjListDist = adjListDist
        self.mobject = mobject

class Dijkstras(MovingCameraScene):
    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png")
        map.scale(0.2).shift(UP*0.2)

        s = Dot(radius = dotRadius, point=LEFT*4.6+UP*1.47, color=color1)
        
        a = Dot(radius = dotRadius, point=LEFT*3.5+UP*1.34, color=color2)
        b = Dot(radius = dotRadius, point=LEFT*3.9+UP*1.1, color=color2)
        

        c = Dot(radius = dotRadius, point=LEFT*3.3+UP*0.7, color=color3)
        d = Dot(radius = dotRadius, point=LEFT*3.9+UP*0.3, color=color3)
        e = Dot(radius = dotRadius, point=LEFT*2.8+UP*1.4, color=color3)
        
        f = Dot(radius = dotRadius, point=LEFT*2.6+UP*0.8, color=color3)
        # g = Dot(radius = dotRadius, point=LEFT*3.15+UP*0.2, color=color3)
        # h = Dot(radius = dotRadius, point=LEFT*3.7+DOWN*0.2, color=color3)
        

        i = Dot(radius = dotRadius, point=LEFT*2.4+UP*2, color=color4)
        j = Dot(radius = dotRadius, point=LEFT*1.7+UP*1.35, color=color4)
        
        k = Dot(radius = dotRadius, point=LEFT*2.1+UP*1, color=color4)

        l = Dot(radius = dotRadius, point=LEFT*1.45+UP*0.6, color=color4)
        m = Dot(radius = dotRadius, point=LEFT*2.05+UP*0.3, color=color4)
        n = Dot(radius = dotRadius, point=LEFT*2.6+UP*0, color=color4)   
        # o = Dot(radius = dotRadius, point=LEFT*2+DOWN*0.3, color=color4)

        p = Dot(radius = dotRadius, point=LEFT*3.15+UP*0.1, color=color4)
        q = Dot(radius = dotRadius, point=LEFT*3.2+DOWN*0.5, color=color4)

        r = Dot(radius = dotRadius, point=LEFT*3.9+DOWN*0.7, color=color4)
        # t = Dot(radius = dotRadius, point=LEFT*3.2+DOWN*1.2, color=color4)

        # self.add(map, s, a, b, c, d, e, i, j, k)
        # self.add(map, s, a, b, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t)
        self.add(map, s, a, b, c, d, e, f, i, j, k, l, m, n, p, q, r, s)

