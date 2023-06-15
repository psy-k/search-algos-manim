from manim import *
from collections import deque
from searchGraphData import cities, positions, adjLists, labelDirections

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


class City:
    def __init__(self, name, adjList, mobject):
        self.name = name
        self.adjList = adjList
        # self.adjListDist = adjListDist
        self.mobject = mobject

class SearchBFS(ZoomedScene):
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
                                color=discoveredCityIconCenterColor, 
                                stroke_width=1, 
                                stroke_color=discoveredCityIconBorderColor
                            )
            cityLabels[city] = Tex(city.upper(), color=BLACK).next_to(
                                    mapCities[city], labelDirections[city]).scale(0.3)
            
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
        
        edges = {}
        greyedEdges = {}
        for city in cities:
            for neighbour in adjLists[city]:
                if city+neighbour not in edges.keys():
                    greyedEdges[city+neighbour] = DashedLine(
                        mapCities[city].get_center(), 
                        mapCities[neighbour].get_center(), 
                        color=dashedEdgeColorGreyed,
                        stroke_width = 0.5
                    )
                    edges[city+neighbour] = DashedLine(
                        mapCities[city].get_center(), 
                        mapCities[neighbour].get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 0.5
                    )
                    edges[neighbour+city] = edges[city+neighbour]
                    greyedEdges[neighbour+city] = greyedEdges[city+neighbour]

                    edges[city+neighbour].set_z_index(greyedEdges[city+neighbour].z_index+1)
                    
                    mapCities[city].set_z_index(edges[city+neighbour].z_index+1)
                    mapCities[neighbour].set_z_index(edges[city+neighbour].z_index+1)

                    self.add(greyedEdges[city+neighbour])
            self.add(mapCities[city], cityLabels[city])


        self.camera.frame.scale(0.5).shift(LEFT*3+UP*0.5)

        startInfo = Tex("Start: S", color = BLACK).scale(0.3).shift(LEFT*5.8+UP*2)
        destInfo = Tex("To Reach: T", color = BLACK).scale(0.3).next_to(startInfo, DOWN).shift(RIGHT*0.15+UP*0.15)

        self.add(startInfo, destInfo)



        
        #-----------BFS----------------
        # what a shame lmao
        start = 's'
        target = 't'
        
        mapCities[start].stroke_color = visitedCityIconBorderColor
        mapCities[start].fill_color = visitedCityIconCenterColor

        mapCities[target].stroke_color = targetCityIconBorderColor
        mapCities[target].fill_color = targetCityIconCenterColor

        visited = []
        discovered = deque()
        curr = start

        prev = []
        discovered += adjLists[curr]
        visited.append(curr)
        mapPin.set_z_index(mapCities['q'].z_index + 1)
        mapPin.move_to(mapCities[start].get_center()+UP*0.1)




        
        self.wait()

        parent = {}
        parent['s'] = None

        pinScale = 1
        offset = UP*0.07

        visitOrder = ['s', 'a', 's', 'b', 's', 'c', 's', 'a', 'h', 'a', 'e', 't']
        

        for i in range(1, len(visitOrder)):
            if visitOrder[i] not in visited:
                visited.append(visitOrder[i])
                if pinScale == 1:
                    self.play(mapPin.animate.scale(0.8).shift(DOWN*0.03), run_time = 0.5)
                    pinScale = 0.5
                # else:
                #     pinScale = 1

                self.play(LaggedStart( *[mapPin.animate.move_to(mapCities[visitOrder[i]].get_center()+offset), 
                                            Create(edges[visitOrder[i-1]+visitOrder[i]])] 
                                        ,lag_ratio=0.2))
                
                if i == len(visitOrder)-1:
                    self.play(
                        mapPin.animate.scale(1/0.8).shift(UP*0.03), 
                        # mapCities[visitOrder[i]].
                        #     animate.set_stroke_color(visitedCityIconBorderColor).
                        #     set_fill_color(visitedCityIconCenterColor),
                        run_time = 0.5
                    )
                else:
                    self.play(
                        # mapPin.animate.scale(2).shift(UP*0.05), 
                        mapCities[visitOrder[i]].
                            animate.
                            # set_stroke_color(visitedCityIconBorderColor).
                            set_fill_color(visitedCityIconCenterColor),
                        run_time = 0.5
                    )

                # self.wait()
            else:
                if pinScale == 1:
                    self.play(mapPin.animate.scale(0.5), run_time = 0.5)
                    pinScale = 0.5

                self.play(mapPin.animate.move_to(mapCities[visitOrder[i]].get_center()+offset))
                # self.wait()

        self.wait(2)
        finalPathColor =  BLUE #"#4ca95e" # "#ffd633" # "#fe4e00" # "#e9190f" # "#09a129" # "#f08700" # "#499f68" 
        prev = ['s', 'a', 'e']
        finalPath = []
        for i in range(1, len(prev)):
            finalPath.append(
                Line(
                    start = mapCities[prev[i-1]].get_center(),
                    end = mapCities[prev[i]].get_center(),
                    color = finalPathColor,
                    stroke_width = 16,
                )
            )
            
            finalPath[i-1].set_z_index(mapCities[prev[i-1]].z_index+1)
            finalPath[i-1].set_opacity(0.5).scale(1.2)
            
            self.play(Create(finalPath[i-1]))

        finalPath.append(
                Line(
                    start = mapCities[prev[-1]].get_center(),
                    end = mapCities[target].get_center(),
                    color = finalPathColor,
                    stroke_width = 16,
                )
            )
            
        finalPath[-1].set_z_index(mapCities[prev[i-1]].z_index+1)
        finalPath[-1].set_opacity(0.5).scale(1.2)
        mapPin.set_z_index(finalPath[-1].z_index+1)
        
        self.play(Create(finalPath[-1]))
        self.wait(2)