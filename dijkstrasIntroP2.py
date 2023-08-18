from manim import *
from collections import deque
from dijkstrasData import cities, positions, labelDirections, adjLists, pathWeights, weightDirections
from dijkstrasLists import *
from dijkstrasHelper import *
from pathKey import *
import json, random
from overlappingAnims import *


UPDATE = "update"
ADD = "add"

class DijkstrasIntroP2_C(ZoomedScene):
    def playAnimsFromList(self, anims, concurrent=False):
        if concurrent:
            animsToPlay = [anims[i] for i in range(len(anims)) if anims[i] != None and anims[i] != KEEP_ORIGINAL]
            self.play(*animsToPlay)
        else:
            for anim in anims:
                if anim == None:
                    self.wait()
                elif anim != KEEP_ORIGINAL:
                    self.play(anim)


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
            GREEN, "Estimated Shortest Path",
            UP*2.2 + LEFT*6.2
        )

        mapCities['s'].set_fill_color(visitedCityIconCenterColor)
        mapCities['t'].set_fill_color(targetCityIconCenterColor)
        mapCities['t'].set_stroke_color(targetCityIconBorderColor)

        mapPin.set_z_index(mapCities['t'].z_index + 1)

        mapPin.move_to(mapCities['s'].get_center() + UP*0.1)
        
        visitedCity = 's'
        target = 't'

        visitedListInitialCities = [
            ListCity("S", "-", 0),
            ListCity("B", "S", 2),
            ListCity("A", "S", 3),
            ListCity("C", "S", 7),
            ListCity("E", "S", 7),
            ListCity("D", "S", 8),
        ]
        discoveredListInitialCities = [
            ListCity("F", "A", 11),
            ListCity("J", "E", 12),
            ListCity("G", "D", 12),
            ListCity("H", "C", 14),
            ListCity("K", "D", 18),
        ]

        mapPin.move_to(mapCities['s'].get_center() + UP*0.1)
        self.add(
            mapCities['s'], mapCities['a'], mapCities['b'], mapCities['c'], 
            mapCities['d'], mapCities['e'], mapCities['f'], 
            cityLabels['s'], cityLabels['a'], cityLabels['b'], cityLabels['c'], 
            cityLabels['d'], cityLabels['e'], cityLabels['f'], 
            greyedEdges['sa'], greyedEdges['sb'], greyedEdges['ba'], greyedEdges['bc'], 
            greyedEdges['bd'], greyedEdges['af'], greyedEdges['ae'], 
            greyedWeights['sa'], greyedWeights['sb'], greyedWeights['ba'], greyedWeights['bc'], 
            greyedWeights['bd'], greyedWeights['af'], greyedWeights['ae'], 
            visitedList.box, discoveredList.box,
            mapPin,
        )

        
        undiscoveredCity = Dot(
                            radius=dotRadius, 
                            point=UP*-0.15 + LEFT*0.2, 
                            color=discoveredCityIconCenterColor, 
                            stroke_width=1, 
                            stroke_color=discoveredCityIconBorderColor
                        )
        undiscoveredCityLabel = Tex("X", color=BLACK).scale(0.3).move_to(undiscoveredCity.get_center() + DOWN*0.15 + RIGHT*0.15)
        undiscoveredCity.set_z_index(undiscoveredCityLabel.z_index+1)

        xNeighbours = ['h', 'g', 'k', 'j']
        xNeighboursParents = ['c', 'd', 'd', 'e']
        hypotheticalEdges = {}
        xEdges = {}
        xEdges['xf'] = DashedLine(
                    undiscoveredCity.get_center(), 
                    mapCities['f'].get_center(), 
                    color=dashedEdgeColor,
                    stroke_width = 0.5
                )
        xEdges['fx'] = xEdges['xf']

        for i in range(len(xNeighbours)):
            neighbour = xNeighbours[i]
            parent  = xNeighboursParents[i]

            hypotheticalEdges[neighbour+parent] = DashedLine(
                                        mapCities[parent].get_center(), 
                                        mapCities[neighbour].get_center(), 
                                        color=BLUE,
                                        stroke_width = 0.5
                                    )
            
            xEdges['x' + neighbour] = DashedLine(
                                        mapCities[neighbour].get_center(), 
                                        undiscoveredCity.get_center(), 
                                        color=BLUE,
                                        stroke_width = 0.5
                                    )
            
            hypotheticalEdges[neighbour+parent].set_z_index(greyedEdges[neighbour+parent].z_index+1)
            xEdges[neighbour + 'x'] = xEdges['x' + neighbour]
            hypotheticalEdges[parent+neighbour] = hypotheticalEdges[neighbour+parent]
        hypotheticalPathKey = PathKey(BLUE, "Hypothetical Path", UP*2.2 + LEFT*6.2,)

        hypotehticalDistances = [
            MarkupText("12 + d<sub>H to X</sub>", color = BLUE).scale(0.2).
                move_to(mapCities['g'].get_center() + DOWN*0.5 + LEFT*0.2),
            MarkupText("12 + d<sub>G to X</sub>", color = BLUE).scale(0.2).
                move_to(mapCities['g'].get_center() + UP*0.15 + RIGHT*0.2),
            MarkupText("14 + d<sub>K to X</sub>", color = BLUE).scale(0.2).
                move_to(mapCities['k'].get_center() + UP*0.15 + LEFT*0.25),
            MarkupText("18 + d<sub>J to X</sub>", color = BLUE).scale(0.2).
                move_to(mapCities['j'].get_center() + DOWN*0.1 + RIGHT*0.6),
        ]


        distanceTxts = ["11",  "<", '12', ',', '12', ',', '14', ',', '18']
        offsets = [
            UP*0, RIGHT*0.05, RIGHT*0.1, 
            RIGHT*0.1+DOWN*0.08, RIGHT*0.1, 
            RIGHT*0.1+DOWN*0.08, RIGHT*0.1, 
            RIGHT*0.1+DOWN*0.08, RIGHT*0.1
        ]
        greaterThanTexts = [
            Text(str(distanceTxts[i]), color=textColor).scale(0.3).shift(LEFT*(0.50-i*0.15) + DOWN*1.8 + offsets[i])
            for i in range(len(distanceTxts))
        ]

        # for mobj in greaterThanTexts:
        #     self.add(mobj)
        
        #-------------------------------------------------------
        #-------------------------------------------------------
        #-----------------------Anims----------------------------
        #-------------------------------------------------------
        #-------------------------------------------------------
        
        self.wait()

        visitedAnims = [
            AnimationGroup(
                LaggedStart(Create(edges['sb']),FadeIn(weights['sb']),lag_ratio = 0.2,),
                LaggedStart(Create(edges['ab']),FadeIn(weights['ab']),lag_ratio = 0.2,),
                LaggedStart(Create(edges['cb']),FadeIn(weights['cb']),lag_ratio = 0.2,),
                LaggedStart(Create(edges['db']),FadeIn(weights['db']),lag_ratio = 0.2,),
                LaggedStart(Create(edges['ae']),FadeIn(weights['ae']),lag_ratio = 0.2,),
                mapCities['s'].animate.set_fill_color(visitedCityIconCenterColor),
                mapCities['a'].animate.set_fill_color(visitedCityIconCenterColor),
                mapCities['b'].animate.set_fill_color(visitedCityIconCenterColor),
                mapCities['c'].animate.set_fill_color(visitedCityIconCenterColor),
                mapCities['d'].animate.set_fill_color(visitedCityIconCenterColor),
                mapCities['e'].animate.set_fill_color(visitedCityIconCenterColor),
            ),
        ]
        anims = visitedList.addCities(
                        visitedListInitialCities, FADEIN, cityLabels, fadeInTogether=True
                    ) 
        visitedAnims.append(AnimationGroup(*anims))

        self.play(LaggedStart(*visitedAnims, lag_ratio=0.2))
        self.wait()
        self.play(FadeIn(shortestPathFoundKey.key))

        self.wait()

        discoveredAnims = [
            AnimationGroup(GrowFromCenter(mapCities["g"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["g"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["h"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["h"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["k"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["k"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["j"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["j"], rate_func= rate_functions.ease_out_back)),

            Create(greyedEdges['ej']),
            Create(greyedEdges['ch']),
            Create(greyedEdges['gd']),
            Create(greyedEdges['kd']),
            Create(greyedWeights['ej']),
            Create(greyedWeights['ch']),
            Create(greyedWeights['gd']),
            Create(greyedWeights['kd']),      
        ]

        anims = discoveredList.addCities(
                        discoveredListInitialCities, FADEIN, cityLabels, fadeInTogether=True
                    )
        discoveredAnims.append(AnimationGroup(*anims))

        self.play(LaggedStart(*discoveredAnims, lag_ratio=0.2))
        self.wait()
        self.play(FadeIn(discoveredPathKey.key))

        self.wait()


        rect1 = SurroundingRectangle(discoveredList.cityVGroups2[0], color = BLUE, buff=0.15)
        rect2 = SurroundingRectangle(discoveredList.cityDistanceMobjects[0], color = RED)
        shortestPossiblePathText = Paragraph(
           "Shortest",
           "Possible",
           "Path",
           alignment="center",
           color = BLUE,
        ).scale(0.2).move_to(edges['af'].get_center() + LEFT*0.35 + DOWN*0.25)


        #
        # Choice explain
        #
        self.play(Create(rect1))
        self.wait()
        self.play(Create(rect2))
        self.wait()
        prev = ['s', 'b', 'a', 'f']
        finalPath = []
        for i in range(len(prev)-1):
            finalPath.append(
                Line(
                    start = mapCities[prev[i]].get_center(),
                    end = mapCities[prev[i+1]].get_center(),
                    color = BLUE,
                    stroke_width = 16,
                )
            )
            
            finalPath[i].set_z_index(mapCities[prev[i]].z_index+1)
            finalPath[i].set_opacity(0.5).scale(1.2)
            mapPin.set_z_index(finalPath[i].z_index+1)
            
            self.play(Create(finalPath[i]))
        self.play(FadeIn(shortestPossiblePathText))
        self.wait()
        self.play(
            Uncreate(finalPath[0]), Uncreate(finalPath[1]), Uncreate(finalPath[2]), 
            FadeOut(shortestPossiblePathText),
            Uncreate(rect1), Uncreate(rect2)
        )
        self.wait()

        # noOfDiscoveredCities = len(discoveredList.cityVGroups2)
        # discoveredCitiesAnims = []
        # alreadyDiscovered = ['b', 'j', 'k', 'g', 'h']
        # for i in range(1, noOfDiscoveredCities):
        #     discoveredCitiesAnims.append(
        #         AnimationGroup(
        #             ScaleInPlace(
        #                 mapCities[alreadyDiscovered[i]],
        #                 1.2,
        #                 rate_func = rate_functions.there_and_back
        #             ),
        #             ScaleInPlace(
        #                 discoveredList.cityNameMobjects[i],
        #                 1.2,
        #                 rate_func = rate_functions.there_and_back
        #             ),
        #             ScaleInPlace(
        #                 discoveredList.cityDistanceMobjects[i],
        #                 1.2,
        #                 rate_func = rate_functions.there_and_back
        #             ),
        #         )
        #     )

        # self.play(LaggedStart(*discoveredCitiesAnims, lag_ratio=0.2))
        # self.wait()

        # discoveredCitiesDistAnims = []
        # for i in range(1, noOfDiscoveredCities):
        #     discoveredCitiesDistAnims.append(
        #             ScaleInPlace(
        #                 discoveredList.cityDistanceMobjects[i],
        #                 1.2,
        #             )
        #     )

        # self.play(LaggedStart(*discoveredCitiesDistAnims, lag_ratio=0.2))
        # self.wait()

        # greaterThanAnims = []
        # for i in range(len(discoveredList.cityDistanceMobjects)):
        #     greaterThanAnims.append(
        #         TransformFromCopy(discoveredList.cityDistanceMobjects[i], greaterThanTexts[2*i]),
        #     )
        #     if i != len(discoveredList.cityDistanceMobjects)-1:
        #         greaterThanAnims.append(FadeIn(greaterThanTexts[2*i+1]))
        # self.play(LaggedStart(*greaterThanAnims), lag_ratio = 0.15)

        # self.wait()

        # resetAnims = []
        # for i in range(1, noOfDiscoveredCities):
        #     resetAnims.append(
        #         ScaleInPlace(discoveredList.cityDistanceMobjects[i], 1/1.2)
        #     )
        # for i in range(len(greaterThanTexts)):
        #     resetAnims.append(FadeOut(greaterThanTexts[i]))
        # self.play(*resetAnims)
        # self.wait()


        # self.play(
        #     LaggedStart(
        #         AnimationGroup(
        #             GrowFromCenter(undiscoveredCity), 
        #             GrowFromCenter(undiscoveredCityLabel),
        #         ),
        #         Create(xEdges['fx'], run_time = 0.7),
        #         lag_ratio=0.6
        #     )
        # )
        # self.wait()

        # anims = []
        # for i in range(len(xNeighbours)):
        #     neighbour = xNeighbours[i]
        #     parent  = xNeighboursParents[i]

        #     anims.append(
        #         LaggedStart(
        #             Create(hypotheticalEdges[neighbour+parent]),
        #             Create(xEdges[neighbour+'x']),
        #             lag_ratio=1
        #         )
        #     )
        # self.play(LaggedStart(*anims, lag_ratio=0.3), FadeIn(hypotheticalPathKey.key))
        # self.wait()

        # anims = []
        # indices = [3, 2, 4, 1]
        # for i in range(len(xNeighbours)):
        #     anims.append(
        #         LaggedStart(
        #             TransformFromCopy(discoveredList.cityDistanceMobjects[indices[i]], hypotehticalDistances[i][:2]),
        #             FadeIn(hypotehticalDistances[i][2:3]),
        #             FadeIn(hypotehticalDistances[i][3:]),
        #             lag_ratio = 0.3,
        #         )
        #     )
        
        # self.play(LaggedStart(*anims, lag_ratio = 0.3))
        # self.wait()

        # resetAnims = [
        #     Uncreate(hypotheticalEdges['ch']), Uncreate(hypotheticalEdges['dg']), 
        #     Uncreate(hypotheticalEdges['dk']), Uncreate(hypotheticalEdges['ej']), 
        #     Uncreate(xEdges['xf']), Uncreate(xEdges['xj']), Uncreate(xEdges['xh']), 
        #     Uncreate(xEdges['xg']), Uncreate(xEdges['xk']),
        #     ShrinkToCenter(undiscoveredCity, rate_func = rate_functions.ease_in_back),
        #     ShrinkToCenter(undiscoveredCityLabel, rate_func = rate_functions.ease_in_back),
        #     FadeOut( *[hypotehticalDistances[i] for i in range(4)]),
        #     FadeOut(hypotheticalPathKey.key)
        # ]
        # self.play(*resetAnims)
        # self.wait()



        # 
        # Visit
        # Update k, j, 
        # Add o
        #
        nextCity = discoveredList.cities[0]

        anims = discoveredList.removeFirstEntry()
        # self.playAnimsFromList(anims)
        
        anims += visitedList.addCities([nextCity], ZOOM, cityLabels)
        # self.playAnimsFromList(anims)
        self.wait()


        moveToNextAnims = []
        moveToNextAnims += [
            LaggedStart(
            mapPin.animate.move_to(mapCities['f'].get_center() + UP*0.1),
            Create(edges['af']),FadeIn(weights['af']),
            lag_ratio=0.15,
            )
        ]
        
        path = ['s', 'b', 'a', 'f']
        movePinAnims = []
        for index in range(len(path)-1):
            # self.play(
            movePinAnims.append(
                mapPin.animate.move_to(mapCities[path[index]].get_center() + UP*0.1)
            )
        movePinAnims += [
            LaggedStart(
            mapPin.animate.move_to(mapCities['f'].get_center() + UP*0.1),
            Create(edges['af']),FadeIn(weights['af']),
            lag_ratio=0.15,
            )
        ]

        self.play(
            LaggedStart(*anims, lag_ratio=1),
            LaggedStart(*movePinAnims, lag_ratio=1)
        )


        # self.playAnimsFromList()
        self.play(mapCities[nextCity.name.lower()].animate.set_fill_color(visitedCityIconCenterColor))
        self.wait()


        # neighbours = []
        # actions = []
        # createEdgesAnims = []
        # discoverCitiesAnims = []
        # visited = ['s', 'b', 'a', 'c', 'd', 'e']
        # discovered = ['f', 'j', 'k', 'g', 'h']
        # edgesOnScreen = ['af']
        # for city in adjLists[nextCity.name.lower()]:
        #     edgeKey = city + nextCity.name.lower()
        #     revEdgeKey = nextCity.name.lower() + city
        #     if edgeKey not in edgesOnScreen:
        #         createEdgesAnims.append(
        #             LaggedStart(
        #                 Create(greyedEdges[edgeKey]),
        #                 FadeIn(greyedWeights[edgeKey]),
        #                 lag_ratio = 0.2
        #             )
        #         )
        #         edgesOnScreen.append(edgeKey)
        #         edgesOnScreen.append(revEdgeKey)
        #     if city not in visited:
                
        #         if city not in discovered:
        #             neighbours.append(
        #                 ListCity(
        #                     city.upper(),
        #                     nextCity.name,
        #                     nextCity.distance + pathWeightsDict[nextCity.name.lower() + city]
        #                 )
        #             )
        #             actions.append(ADD)
        #             discovered.append(city)
        #             discoverCitiesAnims.append(
        #                 AnimationGroup(
        #                     GrowFromCenter(mapCities[city]),
        #                     GrowFromCenter(cityLabels[city])
        #                 )
        #             )
        #         else:
        #             neighbours.append(city.upper())
        #             actions.append(UPDATE)

        # neighbouringAnims = discoverCitiesAnims + createEdgesAnims

        # if len(neighbouringAnims) > 0:
        #     self.play(*neighbouringAnims)
        #     self.wait()
        
        # for i in range(len(neighbours)):
        #     if actions[i] == ADD:
        #         addAnims = discoveredList.addCities([neighbours[i]], FADEIN, cityLabels)
        #         distanceAsSumAnims = discoveredList.showDistanceAsSum(
        #             len(discoveredList.cities)-1,
        #             nextCity.distance,
        #             pathWeightsDict[nextCity.name.lower() + neighbours[i].name.lower()],
        #             nextCity.name,
        #             visitedList.cityDistanceMobjects[-1],
        #             greyedWeights[nextCity.name.lower() + neighbours[i].name.lower()],
        #             onNewCityAdded=True
        #         )
        #         anims = []
        #         anims.append(addAnims[0])
        #         anims += distanceAsSumAnims[:-2]
        #         anims.append(addAnims[1])
        #         anims += distanceAsSumAnims[-2:]
        #         edgeKey = neighbours[i].name.lower() + nextCity.name.lower()
        #     elif actions[i] == UPDATE:
        #         distanceAsSumAnims = discoveredList.updateDistance(
        #             neighbours[i],
        #             nextCity.distance,
        #             pathWeightsDict[nextCity.name.lower() + neighbours[i].lower()],
        #             nextCity.name,
        #             cityLabels[neighbours[i].lower()],
        #             visitedList.cityDistanceMobjects[-1],
        #             greyedWeights[nextCity.name.lower() + neighbours[i].lower()],
        #         )
        #         anims = distanceAsSumAnims

        #     self.playAnimsFromList(anims)
        #     self.wait()

        #     sortAnims = discoveredList.sortList()
        #     self.playAnimsFromList(sortAnims)
        #     self.wait()



        self.wait(2)