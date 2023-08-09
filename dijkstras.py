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

class DijkstrasLogic(ZoomedScene):
    def playAnimsFromList(self, anims, concurrent=False):
        if concurrent:
            animsToPlay = [anims[i] for i in range(len(anims)) if anims[i] != None]
            self.play(*animsToPlay)
        else:
            for anim in anims:
                if anim == None:
                    self.wait()
                else:
                    self.play(anim)


    def construct(self):
        # map = ImageMobject("../maps/dijkstrasMap.png")
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
        # self.add(mapPin)
        # self.add(number_plane, mapPin)

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


        self.add(visitedList.box)
        self.add(discoveredList.box)
        # for group in discoveredList.cityVGroups2:
        #     self.add(group)


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


        visited = ['s']
        discovered = ['a', 'b']
        edgesOnScreen = ['sa', 'as', 'sb', 'bs']

        shortestPathKeyOnScreen = False

        def visitNextCity():
            nonlocal shortestPathKeyOnScreen 

            nextCity = discoveredList.cities[0]
            visited.append(nextCity.name.lower())
            discovered.remove(nextCity.name.lower())


            anims = discoveredList.removeFirstEntry()
            self.playAnimsFromList(anims)
            
            anims = visitedList.addCities([nextCity], ZOOM, cityLabels)
            self.playAnimsFromList(anims)
            self.wait()


            moveToNextAnims = []
            if shortestPathKeyOnScreen == False:
                moveToNextAnims += [FadeIn(shortestPathFoundKey.key)]
                shortestPathKeyOnScreen = True
            

            # movePinToCityAnims = getMovePinToCityAnims(nextCity.name, mapCities, mapPin)

            moveToNextAnims += [
                LaggedStart(
                # movePinToCityAnims[-1],
                mapPin.animate.move_to(mapCities[nextCity.name.lower()].get_center() + UP*0.1),
                Create(edges[nextCity.parent.lower() + nextCity.name.lower()]),
                FadeIn(weights[nextCity.parent.lower() + nextCity.name.lower()]),
                lag_ratio=0.15,
                )
            ]
            
            # print(movePinToCityAnims)
            # print(movePinToCityAnims[:-1])
            path = pathToCity[nextCity.name.lower()]
            for index in range(len(path)-1):
                self.play(
                    mapPin.animate.move_to(mapCities[path[index]].get_center() + UP*0.1)
                )
            # for i in range(len(movePinToCityAnims) -1):
            #     self.play(movePinToCityAnims[i])
            # self.playAnimsFromList(movePinToCityAnims[:-1])

            self.playAnimsFromList(moveToNextAnims, concurrent=True)
            self.play(mapCities[nextCity.name.lower()].animate.set_fill_color(visitedCityIconCenterColor))
            self.wait()


            deadEnd = True
            neighbours = []
            actions = []
            createEdgesAnims = []
            discoverCitiesAnims = []
            for city in adjLists[nextCity.name.lower()]:
                edgeKey = city + nextCity.name.lower()
                revEdgeKey = nextCity.name.lower() + city
                if edgeKey not in edgesOnScreen:
                    createEdgesAnims.append(
                        LaggedStart(
                            Create(greyedEdges[edgeKey]),
                            FadeIn(greyedWeights[edgeKey]),
                            lag_ratio = 0.2
                        )
                    )
                    edgesOnScreen.append(edgeKey)
                    edgesOnScreen.append(revEdgeKey)
                if city not in visited:
                    deadEnd = False
                    
                    if city not in discovered:
                        neighbours.append(
                            ListCity(
                                city.upper(),
                                nextCity.name,
                                nextCity.distance + pathWeightsDict[nextCity.name.lower() + city]
                            )
                        )
                        actions.append(ADD)
                        discovered.append(city)
                        discoverCitiesAnims.append(
                            AnimationGroup(
                                GrowFromCenter(mapCities[city]),
                                GrowFromCenter(cityLabels[city])
                            )
                        )
                    else:
                        neighbours.append(city.upper())
                        actions.append(UPDATE)

            neighbouringAnims = discoverCitiesAnims + createEdgesAnims

            if len(neighbouringAnims) > 0:
                self.play(*neighbouringAnims)
                self.wait()

            if nextCity.name.lower() == 'b':
                self.play(ScaleInPlace(greyedWeights['bc'], 1.5, rate_func = rate_functions.there_and_back))
                self.wait()
                self.play(ScaleInPlace(visitedList.cityDistanceMobjects[1], 1.5, rate_func = rate_functions.there_and_back))
                self.wait()

                
            
            for i in range(len(neighbours)):
                if actions[i] == ADD:
                    addAnims = discoveredList.addCities([neighbours[i]], FADEIN, cityLabels)
                    distanceAsSumAnims = discoveredList.showDistanceAsSum(
                        len(discoveredList.cities)-1,
                        nextCity.distance,
                        pathWeightsDict[nextCity.name.lower() + neighbours[i].name.lower()],
                        nextCity.name,
                        visitedList.cityDistanceMobjects[-1],
                        greyedWeights[nextCity.name.lower() + neighbours[i].name.lower()],
                        onNewCityAdded=True
                    )
                    anims = []
                    anims.append(addAnims[0])
                    anims += distanceAsSumAnims[:-2]
                    anims.append(addAnims[1])
                    anims += distanceAsSumAnims[-2:]
                    edgeKey = neighbours[i].name.lower() + nextCity.name.lower()
                    anims += [
                        None, 
                        LaggedStart(
                            Create(estimatedShortestPathEdges[edgeKey]),
                            FadeIn(estimatedShortestPathWeights[edgeKey]),
                            lag_ratio = 0.2
                        )
                    ]
                elif actions[i] == UPDATE:
                    oldPar, oldDist = getParentAndDistance(discoveredList.cities, neighbours[i])
                    distanceAsSumAnims = discoveredList.updateDistance(
                        neighbours[i],
                        nextCity.distance,
                        pathWeightsDict[nextCity.name.lower() + neighbours[i].lower()],
                        nextCity.name,
                        cityLabels[neighbours[i].lower()],
                        visitedList.cityDistanceMobjects[-1],
                        greyedWeights[nextCity.name.lower() + neighbours[i].lower()],
                    )
                    anims = distanceAsSumAnims
                    newPar, newDist = getParentAndDistance(discoveredList.cities, neighbours[i])

                    if newDist < oldDist:
                        anims += [
                            None,
                            LaggedStart(
                                AnimationGroup(
                                Uncreate(estimatedShortestPathEdges[neighbours[i].lower() + oldPar.lower()]),
                                FadeOut(estimatedShortestPathWeights[neighbours[i].lower() + oldPar.lower()])
                                ),
                                AnimationGroup(
                                Create(estimatedShortestPathEdges[neighbours[i].lower() + newPar.lower()]),
                                FadeIn(estimatedShortestPathWeights[neighbours[i].lower() + newPar.lower()])
                                ),
                                lag_ratio=0.2
                            )
                        ]

                self.playAnimsFromList(anims)
                self.wait()

                sortAnims = discoveredList.sortList()
                self.playAnimsFromList(sortAnims)
                self.wait()

            return nextCity.name.lower()
        
        
        mapCities['s'].set_fill_color(visitedCityIconCenterColor)
        mapCities['s'].set_stroke_color(visitedCityIconBorderColor)
        mapCities['t'].set_fill_color(targetCityIconCenterColor)
        mapCities['t'].set_stroke_color(targetCityIconBorderColor)
        mapPin.set_z_index(mapCities['t'].z_index + 1)

        mapPin.move_to(mapCities['s'].get_center() + UP*0.1)
        # self.add(mapCities['s'])#, cityLabels['s'])
        
        visitedCity = 's'
        target = 't'

        self.wait()
        addSAnims = visitedList.addCities(
            [ListCity("S", "-", 0)],
            FADEIN,
            cityLabels,
            fadeInTogether= True
        )
        addSAnims.append(GrowFromCenter(mapPin))
        addSAnims.append(
            AnimationGroup(
                GrowFromCenter(cityLabels['s']),
                GrowFromCenter(mapCities['s']),
            )
        )
        self.playAnimsFromList(addSAnims,concurrent=True)

        self.wait()

        # self.play(
        #     GrowFromCenter(mapCities['b']),
        #     GrowFromCenter(mapCities['a']),
        #     GrowFromCenter(cityLabels['b']),
        #     GrowFromCenter(cityLabels['a']),
        #     Create(greyedEdges['sa']),
        #     Create(greyedEdges['sb']),
        #     FadeIn(discoveredPathKey.key),
        # )
        # self.wait()
        
        addCitiesAnims = discoveredList.addCities(
            [
                ListCity("A", "S", 4),
                ListCity("B", "S", 2),
            ],
            FADEIN,
            cityLabels,
            fadeInTogether= True
        )
        addCitiesAnims += [
            GrowFromCenter(mapCities['b']),
            GrowFromCenter(mapCities['a']),
            GrowFromCenter(cityLabels['b']),
            GrowFromCenter(cityLabels['a']),
            LaggedStart(Create(greyedEdges['sa']), FadeIn(greyedWeights['sa'])),
            LaggedStart(Create(greyedEdges['sb']), FadeIn(greyedWeights['sb'])),
            # Create(greyedEdges['sb']),
            FadeIn(discoveredPathKey.key),
        ]
        self.playAnimsFromList(addCitiesAnims,concurrent=True)
        self.wait()

        
        estimateAnims = [
            Create(estimatedShortestPathEdges['sb']),
            Create(estimatedShortestPathEdges['sa']),
            FadeIn(estimatedShortestPathWeights['sa']),
            FadeIn(estimatedShortestPathWeights['sb']),
            FadeIn(estimatedShortestPath.key)
        ]
        self.playAnimsFromList(estimateAnims, concurrent=True)
        self.wait()
        
        sortAnims = discoveredList.sortList()
        self.playAnimsFromList(sortAnims, concurrent=True)
        self.wait(2)


        

        # self.wait()
        # visitNextCity()

        while visitedCity != target:
        # for i in range(2):
            visitedCity = visitNextCity().lower()
            self.wait()

        self.wait()
                    
                        





        # self.wait()
        # updateAnims = discoveredList.updateDistance("C", 2, 1, visitedList.cityDistanceMobjects[1], weights['ab'])
        # self.playAnimsFromList(updateAnims)
        # self.wait()
        # anims = discoveredList.sortList()
        # # discoveredList.sortList()
        # self.playAnimsFromList(anims)
        # self.wait()



        # self.wait()
        # for i in range(1, 10):
        #     anims = visitedList.addCities([ListCity(cities[i].upper(), "S", i)], ZOOM)
        #     self.playAnimsFromList(anims)
        #     self.wait()




        # self.wait()
        # anims = discoveredList.addCities(
        #     [
        #         ListCity("B", "S", 4),
        #         ListCity("C", "S", 4),
        #         ListCity("D", "S", 4),
        #         ListCity("E", "S", 4),
        #     ]
        #     , FADEIN
        # )
        # self.playAnimsFromList(anims)
        # self.wait()
        # anims = discoveredList.removeFirstEntry()
        # self.playAnimsFromList(anims)
        # anims = discoveredList.addCities(
        #     [
        #         ListCity("F", "S", 4),
        #         ListCity("G", "S", 4),
        #     ]
        #     , FADEIN
        # )
        # self.playAnimsFromList(anims)
        # self.wait(2)






        
