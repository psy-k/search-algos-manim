from manim import *
from dijkstrasData import cities, positions, labelDirections, adjLists, pathWeights, weightDirections, pathToCity

discoveredCityIconCenterColor = "#c7cbbb"
discoveredCityIconBorderColor= "#7e8a87"

visitedCityIconCenterColor = "#f6edd5"
visitedCityIconBorderColor = "#72472c"

targetCityIconCenterColor = "#ffefaf"
targetCityIconBorderColor = "#ffce00"

dashedEdgeColor = "#b02222"
dashedEdgeColorGreyed = "#7e8a87"
dashedEdgeColorEstimated = BLUE
dotRadius = 0.05


def getDijkstrasMapCitiesAndLabels(altPositions=None, altCityList=None):
    mapCities = {}
    cityLabels = {}
    citiesToUse = cities
    positionsToUse = positions
    
    if altPositions != None:
        positionsToUse = altPositions
    if altCityList != None:
        citiesToUse = altCityList

    for city in citiesToUse:
        mapCities[city] = Dot(
                            radius=dotRadius, 
                            point=positionsToUse[city], 
                            color=discoveredCityIconCenterColor, 
                            stroke_width=1, 
                            stroke_color=discoveredCityIconBorderColor
                        )
        
        cityLabels[city] = Tex(city.upper(), color=BLACK).scale(0.3).next_to(
                                mapCities[city], labelDirections[city])
        cityLabels[city].shift(labelDirections[city]*-0.2)
        
    return mapCities, cityLabels

def getDijkstrasEdgeAndWeightMobjects(mapCities, altCitiesList=None):
    edges = {}
    greyedEdges = {}
    estimatedShortestPathEdges ={}

    pathWeightsDict = {}
    weights = {}
    estimatedShortestPathWeights ={}
    greyedWeights = {}
    for i in range(len(cities)):
        city = cities[i]
        for j in range(len(adjLists[city])):
            neighbour = adjLists[city][j]
            if city+neighbour not in edges.keys():
                greyedEdges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColorGreyed,
                    stroke_width = 0.5
                )
                estimatedShortestPathEdges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColorEstimated,
                    stroke_width = 0.5
                )
                edges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColor,
                    stroke_width = 0.5
                )

                offset = 0.08
                pathWeightsDict[city+neighbour] = pathWeights[city][j]
                greyedWeights[city+neighbour] = Tex(
                                                    str(pathWeights[city][j]), 
                                                    color = dashedEdgeColorGreyed
                                                ).scale(0.3).move_to(
                                                    greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                weights[city+neighbour] = Tex(
                                                str(pathWeights[city][j]), 
                                                color = dashedEdgeColor
                                            ).scale(0.3).move_to(
                                                greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                estimatedShortestPathWeights[city+neighbour] = Tex(
                                                str(pathWeights[city][j]), 
                                                color = dashedEdgeColorEstimated
                                            ).scale(0.3).move_to(
                                                greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                
                edges[neighbour+city] = edges[city+neighbour]
                greyedEdges[neighbour+city] = greyedEdges[city+neighbour]
                estimatedShortestPathEdges[neighbour+city] = estimatedShortestPathEdges[city+neighbour]

                weights[neighbour+city] = weights[city+neighbour]
                greyedWeights[neighbour+city] = greyedWeights[city+neighbour]
                estimatedShortestPathWeights[neighbour+city] = estimatedShortestPathWeights[city+neighbour]
                
                pathWeightsDict[neighbour+city] = pathWeightsDict[city+neighbour]

                estimatedShortestPathEdges[city+neighbour].set_z_index(greyedEdges[city+neighbour].z_index+1)
                edges[city+neighbour].set_z_index(estimatedShortestPathEdges[city+neighbour].z_index+1)

                estimatedShortestPathWeights[city+neighbour].set_z_index(greyedWeights[city+neighbour].z_index+1)
                weights[city+neighbour].set_z_index(estimatedShortestPathWeights[city+neighbour].z_index+1)
                
                mapCities[city].set_z_index(edges[city+neighbour].z_index+1)
                mapCities[neighbour].set_z_index(edges[city+neighbour].z_index+1)

                # self.add(greyedEdges[city+neighbour], weights[city+neighbour])

    return (
        edges, 
        greyedEdges, 
        estimatedShortestPathEdges, 
        pathWeightsDict, 
        weights, 
        estimatedShortestPathWeights,
        greyedWeights
    )

def getParentAndDistance(cities, childCityName):
    for city in cities:
        if city.name == childCityName:
            return city.parent, city.distance
        

def getMovePinToCityAnims(cityInUppercase, mapCities, mapPinMobject):
    targetCity = cityInUppercase.lower()
    path = pathToCity[targetCity] 
    print(path)
    anims = []

    for city in path:
        anims.append(
            mapPinMobject.animate.move_to(mapCities[city].get_center() + UP*0.1)
        )
    
    return anims


def getAltEdgesAndWeights(mapCities):
    edges = {}
    greyedEdges = {}
    estimatedShortestPathEdges ={}

    pathWeightsDict = {}
    weights = {}
    estimatedShortestPathWeights ={}
    greyedWeights = {}
    for i in range(len(cities)):
        city = cities[i]
        for j in range(len(adjLists[city])):
            neighbour = adjLists[city][j]
            if city+neighbour not in edges.keys():
                greyedEdges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColorGreyed,
                    stroke_width = 0.5
                )
                estimatedShortestPathEdges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColorEstimated,
                    stroke_width = 0.5
                )
                edges[city+neighbour] = DashedLine(
                    mapCities[city].get_center(), 
                    mapCities[neighbour].get_center(), 
                    color=dashedEdgeColor,
                    stroke_width = 0.5
                )

                offset = 0.08
                pathWeightsDict[city+neighbour] = pathWeights[city][j]
                greyedWeights[city+neighbour] = Tex(
                                                    str(pathWeights[city][j]), 
                                                    color = dashedEdgeColorGreyed
                                                ).scale(0.3).move_to(
                                                    greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                weights[city+neighbour] = Tex(
                                                str(pathWeights[city][j]), 
                                                color = dashedEdgeColor
                                            ).scale(0.3).move_to(
                                                greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                estimatedShortestPathWeights[city+neighbour] = Tex(
                                                str(pathWeights[city][j]), 
                                                color = dashedEdgeColorEstimated
                                            ).scale(0.3).move_to(
                                                greyedEdges[city+neighbour].get_center() + weightDirections[city][j]*offset)
                
                edges[neighbour+city] = edges[city+neighbour]
                greyedEdges[neighbour+city] = greyedEdges[city+neighbour]
                estimatedShortestPathEdges[neighbour+city] = estimatedShortestPathEdges[city+neighbour]

                weights[neighbour+city] = weights[city+neighbour]
                greyedWeights[neighbour+city] = greyedWeights[city+neighbour]
                estimatedShortestPathWeights[neighbour+city] = estimatedShortestPathWeights[city+neighbour]
                
                pathWeightsDict[neighbour+city] = pathWeightsDict[city+neighbour]

                estimatedShortestPathEdges[city+neighbour].set_z_index(greyedEdges[city+neighbour].z_index+1)
                edges[city+neighbour].set_z_index(estimatedShortestPathEdges[city+neighbour].z_index+1)

                estimatedShortestPathWeights[city+neighbour].set_z_index(greyedWeights[city+neighbour].z_index+1)
                weights[city+neighbour].set_z_index(estimatedShortestPathWeights[city+neighbour].z_index+1)
                
                mapCities[city].set_z_index(edges[city+neighbour].z_index+1)
                mapCities[neighbour].set_z_index(edges[city+neighbour].z_index+1)

                # self.add(greyedEdges[city+neighbour], weights[city+neighbour])

    return (
        edges, 
        greyedEdges, 
        estimatedShortestPathEdges, 
        pathWeightsDict, 
        weights, 
        estimatedShortestPathWeights,
        greyedWeights
    )