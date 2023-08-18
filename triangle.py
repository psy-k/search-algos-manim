from manim import *
from collections import deque
from dijkstrasData import cities, positions, labelDirections, adjLists, pathWeights, weightDirections
from dijkstrasLists import *
from dijkstrasHelper import *
from pathKey import *
import json, random
from overlappingAnims import *

class TriangleIneq(ZoomedScene):

    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png")
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

        mapCities, cityLabels = getDijkstrasMapCitiesAndLabels()


        edgeAndWeightMobjects = getDijkstrasEdgeAndWeightMobjects(mapCities)

        edges = edgeAndWeightMobjects[0]
        greyedEdges = edgeAndWeightMobjects[1] 
        estimatedShortestPathEdges = edgeAndWeightMobjects[2] 
        pathWeightsDict = edgeAndWeightMobjects[3] 
        weights = edgeAndWeightMobjects[4] 
        estimatedShortestPathWeights = edgeAndWeightMobjects[5]
        greyedWeights = edgeAndWeightMobjects[6]

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

        mapPin.set_z_index(mapCities['t'].z_index + 1)
        mapPin.move_to(mapCities['b'].get_center() + UP*0.1)

        mapCities['s'].set_fill_color(visitedCityIconCenterColor)
        mapCities['s'].set_stroke_color(visitedCityIconBorderColor)

        mapCities['b'].set_fill_color(visitedCityIconCenterColor)

        traingleLines = [
            Line(
                mapCities['s'].get_center(), 
                mapCities['a'].get_center(), 
                color=BLACK,
                stroke_width = 0.7
            ),
            Line(
                mapCities['a'].get_center(), 
                mapCities['b'].get_center(), 
                color=BLACK,
                stroke_width = 0.7
            ),
            Line(
                mapCities['b'].get_center(), 
                mapCities['s'].get_center(), 
                color=BLACK,
                stroke_width = 0.7
            ),
        ]
        traingleWeigths = [
            estimatedShortestPathWeights['as'].copy().set_color(BLACK),
            estimatedShortestPathWeights['ab'].copy().set_color(BLACK),
            weights['sb'].copy().set_color(BLACK),
        ]

        traingleLines[0].set_z_index(edges['sb'].z_index + 1)
        traingleLines[1].set_z_index(edges['sb'].z_index + 1)
        traingleLines[2].set_z_index(edges['sb'].z_index + 1)

        mapCities['s'].set_z_index(traingleLines[2].z_index + 1)
        mapCities['a'].set_z_index(traingleLines[2].z_index + 1)
        mapCities['b'].set_z_index(traingleLines[2].z_index + 1)

        mapPin.set_z_index(mapCities['b'].z_index + 1)

        ineqTextScale = 0.4
        ineq = [
            Tex("2", color = BLACK).scale(ineqTextScale).move_to(mapCities['b'].get_center() + DOWN*0.4 + LEFT*0.3),
        ]

        ineq += [
            Text("+", color = BLACK).scale(0.23).move_to(ineq[0].get_center() + RIGHT*0.1),
            Tex("1", color = BLACK).scale(ineqTextScale).move_to(ineq[0].get_center() + RIGHT*0.2),
            Text("<", color = BLACK).scale(0.23).move_to(ineq[0].get_center() + RIGHT*0.35),
            Tex("4", color = BLACK).scale(ineqTextScale).move_to(ineq[0].get_center() + RIGHT*0.5),
            Tex("3", color = BLACK).scale(ineqTextScale).move_to(ineq[0].get_center() + RIGHT*0.2),
        ]

        


        self.add(
            mapPin,
            shortestPathFoundKey.key, estimatedShortestPath.key, discoveredPathKey.key,
            visitedList.box, discoveredList.box,

            mapCities['s'], mapCities['a'], mapCities['b'], mapCities['c'], mapCities['d'],
            cityLabels['s'], cityLabels['a'], cityLabels['b'], cityLabels['c'], cityLabels['d'],

            estimatedShortestPathEdges['as'], edges['sb'], 
            greyedEdges['ba'], greyedEdges['bc'], greyedEdges['bd'],  
            estimatedShortestPathWeights['as'], weights['sb'], 
            greyedWeights['ba'], greyedWeights['bc'], greyedWeights['bd'],  
        )

        anims = visitedList.addCities(
            [ListCity("S", "-", 0), ListCity("B", "S", 2)], 
            cityLabels=cityLabels,
            animType=FADEIN, 
            fadeInTogether=True
        )
        anims += discoveredList.addCities(
            [ListCity("A", "S", 4)],# ListCity("C", "B", 7), ListCity("D", "B", 8)], 
            cityLabels=cityLabels,
            animType=FADEIN, 
            fadeInTogether=True
        )

        self.play(*anims)
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.6).shift(LEFT*1.2 + UP*0.3), 
            FadeOut(
                mapPin, shortestPathFoundKey.key, 
                estimatedShortestPath.key, discoveredPathKey.key,
                
                mapCities['c'], mapCities['d'],
                cityLabels['c'], cityLabels['d'],
                greyedEdges['bc'], greyedEdges['bd'],
                greyedWeights['bc'], greyedWeights['bd'],
            )
        )
        # self.wait()

        borderColor = BLACK
        fill_color = discoveredCityIconCenterColor
        self.play(
            LaggedStart(
                LaggedStart(
                    mapCities['s'].animate.set_stroke_color(borderColor).set_fill_color(fill_color),
                    LaggedStart(
                        Create(traingleLines[0]),
                        FadeIn(traingleWeigths[0]),
                        lag_ratio= 0.2
                    ),
                    lag_ratio= 0.4
                ),
                LaggedStart(
                    mapCities['a'].animate.set_stroke_color(borderColor).set_fill_color(fill_color),
                    LaggedStart(
                        Create(traingleLines[1]),
                        FadeIn(traingleWeigths[1]),
                        lag_ratio= 0.2
                    ),
                    lag_ratio= 0.4
                ),
                LaggedStart(
                    mapCities['b'].animate.set_stroke_color(borderColor).set_fill_color(fill_color),
                    LaggedStart(
                        Create(traingleLines[2]),
                        FadeIn(traingleWeigths[2]),
                        lag_ratio= 0.2
                    ),
                    lag_ratio= 0.4
                ),
                lag_ratio= 0.6
            )
        )


        self.play(
            LaggedStart(
                TransformFromCopy(traingleWeigths[2], ineq[0]),
                FadeIn(ineq[1]),
                TransformFromCopy(traingleWeigths[1], ineq[2]),
                FadeIn(ineq[3]),
                TransformFromCopy(traingleWeigths[0], ineq[4]),
                lag_ratio = 0.5
            )
        )
        sumGroup = VGroup(ineq[0], ineq[1], ineq[2])
        self.play(
            ReplacementTransform(sumGroup, ineq[5])
        )

        self.wait()
        self.play(FadeOut(ineq[5], ineq[4], ineq[3]))
        self.wait(2)

        self.play(
            self.camera.frame.animate.scale(1/0.6).shift(RIGHT*1.2 + DOWN*0.3), 
            FadeOut(
                traingleLines[0], traingleLines[1], traingleLines[2],
                traingleWeigths[0], traingleWeigths[1], traingleWeigths[2],
            ),
            mapCities['s'].animate.set_stroke_color(visitedCityIconBorderColor).set_fill_color(visitedCityIconCenterColor),
            mapCities['a'].animate.set_stroke_color(discoveredCityIconBorderColor).set_fill_color(discoveredCityIconCenterColor),
            mapCities['b'].animate.set_stroke_color(discoveredCityIconBorderColor).set_fill_color(visitedCityIconCenterColor),
            FadeIn(
                mapPin, shortestPathFoundKey.key, 
                estimatedShortestPath.key, discoveredPathKey.key,
                
                mapCities['c'], mapCities['d'],
                cityLabels['c'], cityLabels['d'],
                greyedEdges['bc'], greyedEdges['bd'],
                greyedWeights['bc'], greyedWeights['bd'],
            )
        )

        self.wait(2)