from manim import *
from collections import deque
from aStarData import cities, positions, labelDirections, adjLists, pathWeights, weightDirections
from dijkstrasLists import *
from dijkstrasHelper import *
from pathKey import *
from overlappingAnims import *

start = 's'
target = 't'

class Map:
    def __init__(
        self, mapCities, cityLabels, 
        edges, greyedEdges, estimatedShortestPathEdges, 
        weights, greyedWeights, estimatedShortestPathWeights, 
    ):
        self.mapCities = mapCities
        self.cityLabels = cityLabels
        self.edges = edges
        self.greyedEdges = greyedEdges
        self.estimatedShortestPathEdges = estimatedShortestPathEdges
        self.weights = weights
        self.greyedWeights = greyedWeights
        self.estimatedShortestPathWeights = estimatedShortestPathWeights




class AStar(ZoomedScene):

    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png")
        # map = ImageMobject("../maps/altMap1.png")
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
        self.camera.frame.scale(0.75).shift(LEFT*1.2 + UP*0.2)

        maps = []
        mapCities, cityLabels = getDijkstrasMapCitiesAndLabels(altPositions=positions)
        mapCities[start].set_stroke_color(visitedCityIconBorderColor)
        mapCities[target].set_stroke_color(targetCityIconBorderColor)

        edgeAndWeightMobjects = getDijkstrasEdgeAndWeightMobjects(mapCities)

        maps.append(
            Map(
                mapCities, cityLabels, 
                edgeAndWeightMobjects[0], edgeAndWeightMobjects[1], 
                edgeAndWeightMobjects[2], edgeAndWeightMobjects[4], 
                edgeAndWeightMobjects[6], edgeAndWeightMobjects[5], 
            )
        )
        mapPin.set_z_index(maps[0].mapCities[target].z_index + 1)
        mapPin.move_to(maps[0].mapCities[target].get_center() + UP*0.1)

        visitedOffset = RIGHT*2.5 + UP*1.55
        discoveredOffset = RIGHT*2.5 + UP*-1.2


        visitedList = InfoList("Visited", [], visitedOffset)
        discoveredList = InfoList("Discovered", [], discoveredOffset)


        discoveredPathKey = PathKey(
            dashedEdgeColorGreyed, "Discovered Path",
            UP*2.8 + LEFT*6.2,
        )
        shortestPathFoundKey = PathKey(
            dashedEdgeColor, "Shortest Path Found",
            UP*2.5 + LEFT*6.2
        )
        estimatedShortestPath = PathKey(
            BLUE, "Estimated Shortest Path",
            UP*2.2 + LEFT*6.2
        )
        straightLineDist = PathKey(
            RED, "Straight Line Distance",
            UP*2.2 + LEFT*6.2
        )

        number_plane.set_opacity(0.4)
        # self.add(number_plane)

        # self.add(
        #     discoveredPathKey.key, shortestPathFoundKey.key, 
        #     estimatedShortestPath.key, mapPin,
        #     visitedList.box, discoveredList.box,
        # )

        anims = []
        for city in cities:
            if city != 'q' and city != 'r':
                anims.append(
                    AnimationGroup(
                        GrowFromCenter(maps[0].mapCities[city], rate_func = rate_functions.ease_out_back),
                        GrowFromCenter(maps[0].cityLabels[city], rate_func = rate_functions.ease_out_back),
                    )
                )

        self.wait(2)
        
        self.play(Create(number_plane))
        self.play(LaggedStart(*anims, lag_ratio=0.15))




        self.wait()
        self.play(FadeOut(mapPin))
        

        self.wait(2)

        

        
