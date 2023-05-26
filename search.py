from manim import *
from searchGraphData import cities, positions, adjLists, labelDirections

cityIconCenterColor = "#f6edd5"
cityIconBorderColor = "#72472c"
dashedEdgeColor = "#b02222"
dotRadius = 0.05

color1 = RED
color2 = BLUE
color3 = GREEN
color4 = PINK


class City:
    def __init__(self, name, adjList, mobject):
        self.name = name
        self.adjList = adjList
        # self.adjListDist = adjListDist
        self.mobject = mobject

class Search(ZoomedScene):
    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png")
        mapPin = ImageMobject("../maps/mapPin.png")
        map.scale(0.2).shift(UP*0.2)
        mapPin.scale(0.01)

        mapCities = {}
        cityLabels = {}
        for city in cities:
            mapCities[city] = Dot(
                                radius=dotRadius, 
                                point=positions[city], 
                                color=cityIconCenterColor, 
                                stroke_width=1, 
                                stroke_color=cityIconBorderColor
                            )
            cityLabels[city] = Tex(city.upper(), color=BLACK).next_to(
                                    mapCities[city], labelDirections[city]).scale(0.3)
            
            print((labelDirections[city] is UP  or (labelDirections[city] is DOWN)))
            if (labelDirections[city] is UP) or (labelDirections[city] is DOWN):
                cityLabels[city].shift(labelDirections[city]*-1*0.3)
            else:
                cityLabels[city].shift(labelDirections[city]*-1*0.2)
            
        
                                
        
        # edge = DashedLine(mapCities[0].mobject.get_center(), mapCities[1].mobject.get_center(), color="#b02222")
        # mapCities[0].mobject.set_z_index(edge.z_index+1)
        # mapCities[1].mobject.set_z_index(edge.z_index+1)
        # self.camera.auto_zoom()
        # self.add(map, mapCities[0].mobject, mapCities[1].mobject, edge)


        self.add(map, mapPin)

        edgesRecords = {}
        edges = {}
        for city in cities:
            for neighbour in adjLists[city]:
                if ~(city+neighbour in edges) or edgesRecords[city+neighbour] is None:
                    edges[city+neighbour] = DashedLine(
                        mapCities[city].get_center(), 
                        mapCities[neighbour].get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 0.5
                    )
                    edges[neighbour+city] = edges[city+neighbour]
                    self.add(edges[city+neighbour])
                    mapCities[city].set_z_index(edges[city+neighbour].z_index+1)
                    mapCities[neighbour].set_z_index(edges[city+neighbour].z_index+1)
            self.add(mapCities[city], cityLabels[city])


        self.camera.frame.scale(0.5).shift(LEFT*2+UP*0.5)



        

        # s = Dot(radius = dotRadius, point=LEFT*4.6+UP*1.47, color=cityIconCenterColor,stroke_width=1, stroke_color=cityIconBorderColor)
        
        # a = Dot(radius = dotRadius, point=LEFT*3.55+UP*1.9, color=color2)
        # b = Dot(radius = dotRadius, point=LEFT*3.85+UP*1.3, color=color2)
        # c = Dot(radius = dotRadius, point=LEFT*3.9+UP*0.6, color=color2)
        

        # d = Dot(radius = dotRadius, point=LEFT*2.8+UP*1.4, color=color3)
        # e = Dot(radius = dotRadius, point=LEFT*3.25+UP*0.85, color=color3)
        
        # f = Dot(radius = dotRadius, point=LEFT*2.6+UP*0.45, color=color3)
        # g = Dot(radius = dotRadius, point=LEFT*3.15+UP*0.2, color=color3)
        # h = Dot(radius = dotRadius, point=LEFT*3.7+DOWN*0.2, color=color3)
        

        # i = Dot(radius = dotRadius, point=LEFT*2.4+UP*2, color=color4)
        # j = Dot(radius = dotRadius, point=LEFT*1.55+UP*1.2, color=color4)
        
        # k = Dot(radius = dotRadius, point=LEFT*2.4+UP*0.9, color=color4)

        # l = Dot(radius = dotRadius, point=LEFT*1.45+UP*0.6, color=color4)
        # m = Dot(radius = dotRadius, point=LEFT*1+UP*0.1, color=color4)
        # n = Dot(radius = dotRadius, point=LEFT*1.6+UP*0, color=color4)   
        # o = Dot(radius = dotRadius, point=LEFT*2+DOWN*0.3, color=color4)

        # p = Dot(radius = dotRadius, point=LEFT*2.7+DOWN*0.35, color=color4)
        # q = Dot(radius = dotRadius, point=LEFT*3.2+DOWN*0.5, color=color4)

        # r = Dot(radius = dotRadius, point=LEFT*3.9+DOWN*0.7, color=color4)
        # t = Dot(radius = dotRadius, point=LEFT*3.2+DOWN*1.2, color=color4)

        # self.add(map, s, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t)
        

