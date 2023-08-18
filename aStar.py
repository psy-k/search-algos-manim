from manim import *
from collections import deque
# from aStarData import labelDirections, adjLists, pathWeights, weightDirections
# from aStarData import cities as altCities
# from aStarData import positions as altPositions
from dijkstrasLists import *
from dijkstrasHelper import *
from pathKey import *
from overlappingAnims import *

start = 's'
target = 't'
stLineDistColor = RED

onScreenEdges = [
    'as', 'sb', 'ab', 'ae', 'af', 'bc', 'bd', 'ch', 'dg', 'dk',
    'ej', 'fj', 'fk', 'fo', 'gl', 'gm', 'jn', 'in', 'np', 'nt', 'pt'    
]

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




class AStar1(ZoomedScene):

    def construct(self):
        map = ImageMobject("../maps/Laileia_noCityIcons.png")
        # map = ImageMobject("../maps/altMap1.png")
        mapPin = ImageMobject("../maps/mapPin.png")
        map.scale(0.2).shift(UP*0.2)
        mapPin.scale(0.01)

        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 3,
                "stroke_opacity": 0.5
            }
        )

        self.add(map)
        self.camera.frame.scale(0.75).shift(LEFT*1.2 + UP*0.2)

        maps = []
        # mapCities, cityLabels = getDijkstrasMapCitiesAndLabels(altPositions=positions, altCityList=altCities)
        for i in range(2):
            mapCities, cityLabels = getDijkstrasMapCitiesAndLabels()
            mapCities[start].set_stroke_color(visitedCityIconBorderColor)
            mapCities[target].set_stroke_color(targetCityIconBorderColor)
            mapCities[start].set_fill_color(visitedCityIconCenterColor)
            mapCities[target].set_fill_color(visitedCityIconCenterColor)

            edgeAndWeightMobjects = getDijkstrasEdgeAndWeightMobjects(mapCities)

            maps.append(
                Map(
                    mapCities, cityLabels, 
                    edgeAndWeightMobjects[0], edgeAndWeightMobjects[1], 
                    edgeAndWeightMobjects[2], edgeAndWeightMobjects[4], 
                    edgeAndWeightMobjects[6], edgeAndWeightMobjects[5], 
                )
            )

        visitedOffset = RIGHT*2.5 + UP*1.55
        discoveredOffset = RIGHT*2.5 + UP*-1.2


        visitedList = InfoList("Visited", [], visitedOffset)
        discoveredList = InfoList("Discovered", [], discoveredOffset)


        discoveredPathKey = PathKey(
            dashedEdgeColorGreyed, "Discovered Path",
            UP*2.8 + LEFT*6.2,
        )
        straightLineDistKey = PathKey(
            stLineDistColor, "Straight Line Distance",
            UP*2.5 + LEFT*6.2,
            solidLine=True
        )

        qMarks = {}
        for edge in onScreenEdges:
            qMarks[edge] = Text("?", color = DARK_GREY).scale(0.22).move_to(maps[0].greyedEdges[edge].get_center())
            qMarks[edge].set_z_index(maps[0].greyedEdges[edge].z_index + 1)


        stLinesDec = ['s', 'b', 'f', 'j']
        stLinesRandom = []
        dest = maps[0].mapCities['t']
        for i in range(len(stLinesDec)):
            src = maps[0].mapCities[stLinesDec[i]]
            stLinesRandom.append(
                Line(src.get_center(), dest.get_center(), color = stLineDistColor, stroke_width = 0.7)
            )
            src.set_z_index(stLinesRandom[i].z_index + 1)
            dest.set_z_index(stLinesRandom[i].z_index + 1)
        stLineDistLabel = MarkupText(
                            "d<sub>S to T</sub>", color = stLineDistColor
                        ).scale(0.3).move_to(
                            stLinesRandom[0].get_center()
                        ).shift(DOWN*0.2).rotate(stLinesRandom[0].get_angle())
        

        mapPin.set_z_index(maps[0].mapCities[start].z_index + 1)
        mapPin.move_to(maps[0].mapCities[start].get_center() + UP*0.1)

        nbrOrder = [1, 3, 0, 2]
        sNeighbours = ['b', 'q', 'a', 'r']
        stLineDistances = [17, 20, 16, 21]
        stLineMobjects = []
        stLineDistMobjects = []
        stLineDistMobPositions = [
            LEFT*1.1 + UP*0.55,
            LEFT*2.9 + UP*1.2,
            LEFT*0.7 + UP*1.1,
            LEFT*2.4 + UP*1.35,
        ]
        dest = maps[0].mapCities['t']
        # distTextScale = 0.4
        for i in range(len(sNeighbours)):
            src = maps[0].mapCities[sNeighbours[i]]
            stLineMobjects.append(
                Line(src.get_center(), dest.get_center(), color = stLineDistColor, stroke_width = 1)
            )
            stLineDistMobjects.append(
                Tex(str(stLineDistances[i]), color = stLineDistColor).scale(0.3).move_to(stLineDistMobPositions[i])
            )
            src.set_z_index(stLineMobjects[i].z_index + 1)
            dest.set_z_index(stLineMobjects[i].z_index + 1)


        self.wait(2)
        
        xLinesOrder = [3, 2, 1, 0, 4, 5, 6]
        yLinesOrder = [13, 12, 11, 10, 9, 8, 0, 1, 2, 3, 4]
        
        animsX = []
        for i in range(len(xLinesOrder)):
            animsX.append(Create(number_plane.x_lines[xLinesOrder[i]]))
        animsY = []
        for i in range(len(yLinesOrder)):
            animsY.append(Create(number_plane.y_lines[yLinesOrder[i]]))
        
        self.play(
            LaggedStart(
                LaggedStart(*animsX), LaggedStart(*animsY),
                lag_ratio= 0.0, run_time = 2
            )
        )
        self.wait()
        anims = []
        for city in cities:
            maps[0].mapCities[city].set_z_index(number_plane.z_index + 1)
            maps[0].cityLabels[city].set_z_index(number_plane.z_index + 1)
            if city != 'q' and city != 'r':
                anims.append(
                    AnimationGroup(
                        GrowFromCenter(maps[0].mapCities[city], rate_func = rate_functions.ease_out_back),
                        GrowFromCenter(maps[0].cityLabels[city], rate_func = rate_functions.ease_out_back),
                    )
                )
        self.play(LaggedStart(*anims, lag_ratio=0.15, run_time = 2))
        self.wait()

        self.play(
            number_plane.x_lines.animate.set_opacity(0.2),
            number_plane.y_lines.animate.set_opacity(0.2)
        )
        self.wait()


        anims = []
        for edge in onScreenEdges:
            anims.append(Create(maps[1].greyedEdges[edge]))
            anims.append(GrowFromCenter(qMarks[edge], rate_func = rate_functions.ease_out_back))
        # anims.append(number_plane.x_lines.animate.set_opacity(0.2))
        # anims.append(number_plane.y_lines.animate.set_opacity(0.2))
        self.play(*anims)
        self.wait(0.5)

        anims = []
        for edge in onScreenEdges:
            anims.append(Uncreate(maps[1].greyedEdges[edge]))
            anims.append(ShrinkToCenter(qMarks[edge], rate_func = rate_functions.ease_in_back))
        self.play(*anims)
        self.wait()


        self.play(Create(stLinesRandom[0]))
        self.wait()
        self.play(FadeIn(stLineDistLabel))
        # self.play(FadeIn(stLineDistLabel, straightLineDistKey.key))
        self.wait()


        for i in range(1, len(stLinesRandom)):
            anims = [
                LaggedStart(
                    Uncreate(stLinesRandom[i-1]),
                    Create(stLinesRandom[i]),
                    lag_ratio = 0.5
                ),
            ]
            if i == 1:
                anims.append(FadeOut(stLineDistLabel))
            self.play(*anims)

        # self.wait()
        self.play(Uncreate(stLinesRandom[-1]))
        self.wait()

        visitedListAddAnims = visitedList.addCities([ListCity('S', '-', 0)], FADEIN, maps[0].cityLabels, fadeInTogether=True)
        discoveredListAddAnims = discoveredList.addCities(
            [
                ListCity('Q', 'S', 1),
                ListCity('R', 'S', 1),
                ListCity('B', 'S', 2),
                ListCity('A', 'S', 4),
                
            ], 
            # [
            #     ListCity('A', 'S', 4),
            #     ListCity('B', 'S', 2),
            #     ListCity('Q', 'S', 1),
            #     ListCity('R', 'S', 1),
            # ], 
            FADEIN, maps[0].cityLabels, fadeInTogether=True
        )

        for mobj in visitedList.cityVGroups2:
            mobj.set_z_index(visitedList.box.z_index + 2)
        for mobj in discoveredList.cityVGroups2:
            mobj.set_z_index(discoveredList.box.z_index + 2)
        anims = [
            GrowFromCenter(maps[0].mapCities['q'], rate_func = rate_functions.ease_out_back),
            GrowFromCenter(maps[0].mapCities['r'], rate_func = rate_functions.ease_out_back),
            GrowFromCenter(maps[0].cityLabels['q'], rate_func = rate_functions.ease_out_back),
            GrowFromCenter(maps[0].cityLabels['r'], rate_func = rate_functions.ease_out_back),
            GrowFromCenter(mapPin, rate_func = rate_functions.ease_out_back),
            LaggedStart(
                Create(maps[0].greyedEdges['bs']), 
                FadeIn(maps[0].greyedWeights['sb']),
                lag_ratio = 0.2
            ),
            LaggedStart(
                Create(maps[0].greyedEdges['as']), 
                FadeIn(maps[0].greyedWeights['sa']),
                lag_ratio = 0.2
            ),
            LaggedStart(
                Create(maps[0].greyedEdges['sq']), 
                FadeIn(maps[0].greyedWeights['sq']),
                lag_ratio = 0.2
            ),
            LaggedStart(
                Create(maps[0].greyedEdges['sr']), 
                FadeIn(maps[0].greyedWeights['sr']),
                lag_ratio = 0.2
            ),

            LaggedStart(
                FadeIn(visitedList.box, visitedList.heading),
                AnimationGroup(*visitedListAddAnims),
                lag_ratio=0.2
            ),
            LaggedStart(
                FadeIn(discoveredList.box, discoveredList.heading),
                AnimationGroup(*discoveredListAddAnims),
                lag_ratio=0.2
            ),
            
        ]

        
        self.play(*anims)
        self.wait()

        anims = discoveredList.sortList()
        self.play(*anims)
        self.wait()


        anims = []
        for i in range(len(stLineMobjects)):
            anims.append(
                LaggedStart(
                    Create(stLineMobjects[i]),
                    FadeIn(stLineDistMobjects[i]),
                    lag_ratio = 0.2
                )
            )
        self.play(LaggedStart(*anims, lag_ratio = 0.2))
        self.wait()

        addnSigns = []
        listStDistanceMobjects = []
        closeBrackets = []
        openBrackets = []
        listSums = [21, 22, 18, 20]
        listSumMobjects = []
        anims = []
        for i in range(len(sNeighbours)):
            addnSigns.append(
                Text("+", color=BLACK).scale(0.25).shift(UP*(0.70-i*0.3) + RIGHT*0.45 + discoveredOffset)
            )
            listStDistanceMobjects.append(
                Text(
                    str(stLineDistances[nbrOrder[i]]), 
                    color=stLineDistColor
                ).scale(0.25).shift(UP*(0.70-i*0.3) + RIGHT*0.65 + discoveredOffset)
            )
            closeBrackets.append(
                Text(")", color=BLACK).scale(0.25).move_to(listStDistanceMobjects[i].get_center() + RIGHT*0.15)
            )
            openBrackets.append(
                Text("(", color=BLACK).scale(0.25).move_to(discoveredList.cityDistanceMobjects[i].get_center() + LEFT*0.32)
            )
            listSumMobjects.append(
                Text(str(listSums[i]), color=BLACK).scale(0.25).move_to(openBrackets[i].get_center() + LEFT*0.2)
            )
            anims.append(
                LaggedStart(
                    discoveredList.cityDistanceMobjects[i].animate.shift(LEFT*0.22),
                    FadeIn(addnSigns[i]),
                    TransformFromCopy(stLineDistMobjects[nbrOrder[i]], listStDistanceMobjects[i]),
                    FadeIn(listSumMobjects[i], openBrackets[i], closeBrackets[i]),
                    lag_ratio = 0.2,
                )
            )
        
        self.play(LaggedStart(*anims, lag_ratio = 0.2))
        self.wait()

        # closeBrackets = []
        # openBrackets = []
        # listSums = [21, 22, 18, 20]
        # listSumMobjects = []
        # anims = []
        # for i in range(len(sNeighbours)):
        #     closeBrackets.append(
        #         Text(")", color=BLACK).scale(0.25).move_to(listStDistanceMobjects[i].get_center() + RIGHT*0.15)
        #     )
        #     openBrackets.append(
        #         Text("(", color=BLACK).scale(0.25).move_to(discoveredList.cityDistanceMobjects[i].get_center() + LEFT*0.1)
        #     )
        #     listSumMobjects.append(
        #         Text(str(listSums[i]), color=BLACK).scale(0.25).move_to(openBrackets[i].get_center() + LEFT*0.2)
        #     )
        #     anims.append(FadeIn(listSumMobjects[i], openBrackets[i], closeBrackets[i]))
        
        # self.play(LaggedStart(*anims, lag_ratio = 0.2))
        # self.wait()


        shifts = [DOWN*0.3*2, DOWN*0.3*2, UP*0.3*2, UP*0.3*2]
        anims = []
        for i in range(len(discoveredList.cityVGroups2)):
            anims += [
                discoveredList.cityVGroups2[i].animate.shift(shifts[i]), addnSigns[i].animate.shift(shifts[i]),
                openBrackets[i].animate.shift(shifts[i]), closeBrackets[i].animate.shift(shifts[i]), 
                listSumMobjects[i].animate.shift(shifts[i]), listStDistanceMobjects[i].animate.shift(shifts[i]),
            ]

        self.play(*anims)
        self.wait()


        self.play(
            ScaleInPlace(discoveredList.cityDistanceMobjects[0], 1.3, rate_func = rate_functions.there_and_back),
            ScaleInPlace(discoveredList.cityDistanceMobjects[1], 1.3, rate_func = rate_functions.there_and_back)
        )
        self.wait()
        self.play(
            ScaleInPlace(listStDistanceMobjects[0], 1.3, rate_func = rate_functions.there_and_back),
            ScaleInPlace(listStDistanceMobjects[1], 1.3, rate_func = rate_functions.there_and_back)
        )
        self.wait()



        self.wait(2)

        

        
