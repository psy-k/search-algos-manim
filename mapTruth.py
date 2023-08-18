from manim import *
from collections import deque
from dijkstrasData import cities, positions, labelDirections, adjLists, pathWeights, weightDirections
from dijkstrasAltPositionsData import altPositions
from dijkstrasLists import *
from dijkstrasHelper import *
from pathKey import *
import json, random
from overlappingAnims import *
from dataList import DataList, listPositions

start = 's'
target = 't'
visitedCities = [
    "s", "b", "a", "c", "d", "e", "f", "g", 
    "h", "j", "k", "l", "n", "p", "t"
]
onScreenGreyEdges = ['sa']#, 'cd', 'fj', 'dk', 'oj', 'pt']
onScreenEdges = [
    'sb', 'ba', 'bc', 'bd',]
# 'ae', 'af', 'ch', 
#     'dg', 'ej', 'fk', 'gl', 'np', 'nt', 'nj', 
# ]
onScreenEstimatedEdges = []#'in', 'fo', 'gm']

config.background_color = "#04f404"

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

def transformMap(map1, map2):
    anims = []
    for city in cities:
        anims.append(ReplacementTransform(map1.mapCities[city], map2.mapCities[city]))
        anims.append(ReplacementTransform(map1.cityLabels[city], map2.cityLabels[city]))
    for edge in onScreenGreyEdges:
        anims.append(ReplacementTransform(map1.greyedEdges[edge], map2.greyedEdges[edge]))
        anims.append(ReplacementTransform(map1.greyedWeights[edge], map2.greyedWeights[edge]))
    for edge in onScreenEdges:
        anims.append(ReplacementTransform(map1.edges[edge], map2.edges[edge]))
        anims.append(ReplacementTransform(map1.weights[edge], map2.weights[edge]))
    for edge in onScreenEstimatedEdges:
        anims.append(ReplacementTransform(map1.estimatedShortestPathEdges[edge], map2.estimatedShortestPathEdges[edge]))
        anims.append(ReplacementTransform(map1.estimatedShortestPathWeights[edge], map2.estimatedShortestPathWeights[edge]))
    
    return anims

def ScaleMap(map):
    scaleFactor = 1.3
    anims = []
    for city in cities:
        anims.append(ScaleInPlace(map.mapCities[city], scaleFactor, rate_func = rate_functions.there_and_back))
        anims.append(ScaleInPlace(map.cityLabels[city], scaleFactor, rate_func = rate_functions.there_and_back))
    for edge in onScreenGreyEdges:
        # anims.append(ScaleInPlace(map.greyedEdges[edge], scaleFactor, rate_func = rate_functions.there_and_back))
        anims.append(ScaleInPlace(map.greyedWeights[edge], scaleFactor, rate_func = rate_functions.there_and_back))
    for edge in onScreenEdges:
        # anims.append(ScaleInPlace(map.edges[edge], scaleFactor, rate_func = rate_functions.there_and_back))
        anims.append(ScaleInPlace(map.weights[edge], scaleFactor, rate_func = rate_functions.there_and_back))
    for edge in onScreenEstimatedEdges:
        # anims.append(ScaleInPlace(map.estimatedShortestPathEdges[edge], scaleFactor, rate_func = rate_functions.there_and_back))
        anims.append(ScaleInPlace(map.estimatedShortestPathWeights[edge], scaleFactor, rate_func = rate_functions.there_and_back))

    return anims

def listToMapAnims(dataList, mapCopy, city):
    anims = []
    anims.append(FadeIn(dataList.listBox))
    subAnims = []
    subAnims.append(TransformFromCopy(mapCopy.cityLabels[city], dataList.cityHeading))
    # anims.append(TransformFromCopy(dataList.cityHeading, mapCopy.cityLabels[city]))
    for i in range(len(adjLists[city])):
        neighbour = adjLists[city][i]
        edge = city+neighbour
        revEdge = neighbour+city
        if edge in onScreenGreyEdges:
            edgeMobj = mapCopy.greyedWeights[edge]
        elif revEdge in onScreenGreyEdges:
            edgeMobj = mapCopy.greyedWeights[revEdge]
        elif edge in onScreenEdges:
            edgeMobj = mapCopy.weights[edge]
        elif revEdge in onScreenEdges:
            edgeMobj = mapCopy.weights[revEdge]
        elif edge in onScreenEstimatedEdges:
            edgeMobj = mapCopy.estimatedShortestPathWeights[edge]
        elif revEdge in onScreenEstimatedEdges:
            edgeMobj = mapCopy.estimatedShortestPathWeights[revEdge]
        subAnims.append(
            AnimationGroup(
                TransformFromCopy(mapCopy.cityLabels[neighbour], dataList.cityConnectedCities[i]),
                TransformFromCopy(edgeMobj, dataList.cityConnectedCitiesDistances[i]),
                # TransformFromCopy(dataList.cityConnectedCities[i], mapCopy.cityLabels[neighbour]),
                # TransformFromCopy(dataList.cityConnectedCitiesDistances[i], edgeMobj),
            )
        )
    anims.append(AnimationGroup(*subAnims))
    return anims


class MapTruth_2(ZoomedScene):

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

        # self.add(map)
        self.camera.frame.scale(0.75).shift(LEFT*1.2 + UP*0.2)

        maps = []
        for positions in altPositions:
            mapCities, cityLabels = getDijkstrasMapCitiesAndLabels(altPositions=positions)
            for city in visitedCities:
                mapCities[city].set_fill_color(visitedCityIconCenterColor)
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

        number_plane.set_opacity(0.4)
        # self.add(number_plane)

        # self.add(
        #     discoveredPathKey.key, shortestPathFoundKey.key, 
        #     estimatedShortestPath.key, mapPin,
        #     visitedList.box, discoveredList.box,
        # )

        citiesOnScreen = ['s', 'a', 'b', 'c', 'd']
        for city in citiesOnScreen:
            self.add(maps[0].mapCities[city], maps[0].cityLabels[city])
        for edge in onScreenGreyEdges:
            self.add(maps[0].greyedEdges[edge], maps[0].greyedWeights[edge])
        for edge in onScreenEdges:
            self.add(maps[0].edges[edge], maps[0].weights[edge])
        for edge in onScreenEstimatedEdges:
            self.add(maps[0].estimatedShortestPathEdges[edge], maps[0].estimatedShortestPathWeights[edge])

        # for city in cities:
        asListsText = Text("which is in the form of lists", color = BLACK).scale(0.45).shift(LEFT*1.5, UP*2.5)
        textBgRect = BackgroundRectangle(asListsText, WHITE, fill_opacity=0.5, buff=0.1)
        listEllipsesText = Text("...", color = BLACK).scale(0.8).shift(LEFT*-0.4, DOWN*1.7)
        ellipsisBg = BackgroundRectangle(listEllipsesText, WHITE, fill_opacity=0.5, buff=0.1)
        self.wait()



        # anims = discoveredList.addCities(
        #     [
        #         ListCity("I", "N", 19),
        #         ListCity("O", "F", 20),
        #         ListCity("M", "G", 22),
        #     ],
        #     FADEIN, maps[0].cityLabels,
        #     fadeInTogether=True,
        # )
        # anims += visitedList.addCities(
        #     [
        #         ListCity("I", "N", 19), ListCity("A", "S", 19),
        #         ListCity("O", "F", 20), ListCity("B", "S", 19),
        #         ListCity("M", "G", 22), ListCity("C", "S", 19),
        #     ],
        #     FADEIN, maps[0].cityLabels,
        #     fadeInTogether=True,
        # )
        # self.play(*anims)
        # anims = visitedList.addCities([ListCity("K", "F", 14)], ZOOM, maps[0].cityLabels)
        # self.play(*anims)
        # anims = visitedList.addCities([ListCity("L", "G", 14)], ZOOM, maps[0].cityLabels)
        # self.play(*anims)
        # anims = visitedList.addCities([ListCity("N", "J", 16)], ZOOM, maps[0].cityLabels)
        # self.play(*anims)
        # anims = visitedList.addCities([ListCity("P", "N", 17)], ZOOM, maps[0].cityLabels)
        # self.play(*anims)
        # anims = visitedList.addCities([ListCity("T", "N", 18)], ZOOM, maps[0].cityLabels)
        # self.play(*anims)
        # self.wait(2)
        # #-------------------------------------------------------------

        # anims = ScaleMap(maps[0])
        # anims.append(ScaleInPlace(mapPin, 1.3, rate_func = rate_functions.there_and_back))
        # self.wait()
        # self.play(*anims, run_time = 2)

        
        self.wait(2)
        # self.play(FadeIn(textBgRect, asListsText, run_time = 0.5))
        lists = []
        anims = []
        for i in range(2):
            lists.append(DataList(cities[i].upper(), adjLists[cities[i]], pathWeights[cities[i]]))
            lists[i].list.set_z_index(mapPin.z_index + 1).scale(0.6).shift(LEFT*(3.5 - i*2), DOWN*1.7)
            lists[i].cityHeading.set_z_index(lists[i].listBox.z_index + 1)
            lists[i].cityConnectedCities.set_z_index(lists[i].listBox.z_index + 1)
            lists[i].cityConnectedCitiesDistances.set_z_index(lists[i].listBox.z_index + 1)
            anims = listToMapAnims(lists[i], maps[(4+i)%5], cities[i])
            # anims.append(LaggedStart(*animsTemp, lag_ratio = 0))
            if i == 0:
                self.play(FadeIn(textBgRect, asListsText, run_time = 0.5), LaggedStart(*anims, lag_ratio = 0))
            else:
                self.play(LaggedStart(*anims, lag_ratio = 0))
                
            # self.wait()
        # anims.append(FadeIn(ellipsisBg, listEllipsesText, run_time = 0.5))
        # self.play(*anims)
        self.play(FadeIn(ellipsisBg, listEllipsesText, run_time = 0.5))
        self.wait()

        self.play(
            FadeOut(
                lists[0].list, lists[1].list, #lists[2].list,
                ellipsisBg, listEllipsesText, asListsText, textBgRect,
                # maps[4].cityLabels['s'], maps[4].cityLabels['a'], maps[4].cityLabels['b'], 
                # maps[4].cityLabels['c'], maps[4].cityLabels['d'], maps[4].cityLabels['e'], maps[4].cityLabels['f'],
                # maps[4].greyedWeights['as'],
                # maps[4].weights['ab'], maps[4].weights['ae'], maps[4].weights['af'], 
                # maps[4].weights['sb'], maps[4].weights['bc'], maps[4].weights['bd'], 
            )
        )

        self.wait(2)




        # self.wait(3)
        # self.play(FadeOut(mapPin))

        # l = len(altPositions)
        # for i in range(l-1):
        #     print(i)
        #     anims = transformMap(maps[i], maps[i+1])
        #     self.play(*anims)
        #     self.wait()

        # self.wait()

        # vListMobjects = []
        # for i in range(len(visitedList.cityVGroups2)):
        #     obj = visitedList.cityVGroups2[i]
        #     obj.set_z_index(visitedList.heading.z_index + 1)
        #     if i != 0:
        #         vListMobjects.append(obj)
        # vListMobjects += [visitedList.box, visitedList.ellipses,]
        # vList = VGroup(*vListMobjects)
        
        # dListMobjects = []
        # for i in range(len(discoveredList.cityVGroups2)):
        #     obj = discoveredList.cityVGroups2[i]
        #     obj.set_z_index(discoveredList.heading.z_index + 1)
        #     dListMobjects.append(obj)
        # dListMobjects += [discoveredList.box]
        # dList = VGroup(*dListMobjects)
        
        # self.play(
        #     ScaleInPlace(vList, 1.2, rate_func = rate_functions.there_and_back),
        #     ScaleInPlace(dList, 1.2, rate_func = rate_functions.there_and_back),
        # )
        # self.wait()

        

        # self.wait(2)

        

        
