from manim import *
from collections import deque
from dijkstrasData import cities, positions, labelDirections, adjLists
import json, random
from overlappingAnims import *

discoveredCityIconCenterColor = "#c7cbbb"
discoveredCityIconBorderColor= "#7e8a87"

visitedCityIconCenterColor = "#f6edd5"
visitedCityIconBorderColor = "#72472c"

targetCityIconCenterColor = "#ffefaf"
targetCityIconBorderColor = "#ffce00"

dashedEdgeColor = "#b02222"
dashedEdgeColorGreyed = "#7e8a87"
dotRadius = 0.05

color1 = RED
color2 = BLUE
color3 = GREEN
color4 = PINK


class DijkstrasLogic(ZoomedScene):
    def construct(self):
        map = ImageMobject("../maps/dijkstrasMap.png")
        # map = ImageMobject("../maps/Laileia_noCityIcons.png")
        mapPin = ImageMobject("../maps/mapPin.png")
        map.scale(0.2).shift(UP*0.2)
        mapPin.scale(0.01)

        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        )

        self.add(map)

        self.add(number_plane, mapPin)

        mapCities = {}
        citiesGroup = VGroup()
        for city in cities:
            mapCities[city] = Dot(
                                radius=dotRadius, 
                                point=positions[city], 
                                color=visitedCityIconCenterColor, 
                                stroke_width=1, 
                                stroke_color=discoveredCityIconBorderColor
                            )
            # self.add(mapCities[city])

        
        
        edges = {}
        edgesGroup = VGroup()
        for i in range(len(positions)):
            city = cities[i]
            for neighbour in adjLists[city]:
                if city+neighbour not in edges.keys():
                    edges[city+neighbour] = DashedLine(
                        mapCities[city].get_center(), 
                        mapCities[neighbour].get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 0.5
                    )
                    edges[neighbour+city] = edges[city+neighbour]                    
                    mapCities[city].set_z_index(edges[city+neighbour].z_index+1)
                    mapCities[neighbour].set_z_index(edges[city+neighbour].z_index+1)

                    # self.add(edges[str(city)+str(neighbour)])



        
