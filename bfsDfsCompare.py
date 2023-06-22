from manim import *
from collections import deque
from compareData1 import cities, positions, adjLists, labelDirections

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


class CompareDFS2(ZoomedScene):
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

                    # self.add(greyedEdges[city+neighbour])
            # self.add(mapCities[city], cityLabels[city])


        self.camera.frame.scale(0.5).shift(LEFT*3+UP*0.5)
        self.add(
            mapCities["s"], mapCities["a"], mapCities["b"], mapCities["c"],
            cityLabels['s'], cityLabels['a'], cityLabels['b'], cityLabels['c'],
            greyedEdges['sa'], greyedEdges['sb'], greyedEdges['sc'],
            )
        
        onScreen = ['s', 'a', 'b', 'c']
        start = "s"
        mapPin.set_z_index(mapCities[start].z_index+1)
        mapPin.move_to(mapCities[start].get_center()+UP*0.1)
        mapCities[start].set_fill_color(visitedCityIconCenterColor)



        target = "d"

        #-------------------------------DFS----------------------------------
        
        self.wait()
        curr = start

        visited = ['s']
        prev = []

        while target not in adjLists[curr]:
            foundNew = False
            for city in adjLists[curr]:
                if city not in visited:
                    # self.wait()
                    self.play(
                        LaggedStart( 
                            mapPin.animate.move_to(mapCities[city].get_center()+UP*0.1), 
                            Create(edges[curr+city]),
                            lag_ratio = 0.2
                        )
                    )
                    prev.append(curr)
                    curr = city
                    visited.append(city)
                    foundNew = True
                    break

            if foundNew:
                toAdd = []
                for city in adjLists[curr]:
                    if city not in onScreen:
                        toAdd.append(mapCities[city])
                        toAdd.append(cityLabels[city])
                        toAdd.append(greyedEdges[curr+city])
                        onScreen.append(city)
                # self.wait()

                if len(toAdd) > 0:
                    self.play(
                        mapCities[curr].animate.set_fill_color(visitedCityIconCenterColor),
                        FadeIn(*toAdd)
                    )
                else:
                    self.play(
                        mapCities[curr].animate.set_fill_color(visitedCityIconCenterColor),
                    )
            else:
                curr = prev.pop()
                # self.wait()
                self.play(mapPin.animate.move_to(mapCities[curr].get_center()+UP*0.1))
        
        # self.wait()
        self.play(
            LaggedStart( 
                mapPin.animate.move_to(mapCities[target].get_center()+UP*0.1), 
                Create(edges[curr+target]),
                lag_ratio = 0.2
            )
        )
        self.play(
            mapCities[target].animate.
                set_fill_color(targetCityIconCenterColor).
                set_stroke_color(targetCityIconBorderColor),
        )

        self.wait(2)
        

        
        # #-------------------------------BFS----------------------------------
        
        # self.wait()

        # visited = ['s']
        # # order = ['s', 'a', 's', 'b', 's', 'c', 's', 
        # #          'a', 'h', 'a', 'e', 'a', 's', 
        # #          'b', 'g', 'b', 'd', 'b', 's', 
        # #          'a', 'h', 'r', 'h', 'q']
        # order = ['s', 'a', 's', 'b']

        # for i in range(1, len(order)):
        #     city = order[i]
        #     if city not in visited:
        #         self.play(
        #             LaggedStart( 
        #                 mapPin.animate.move_to(mapCities[city].get_center()+UP*0.1), 
        #                 Create(edges[order[i-1]+city]),
        #                 lag_ratio = 0.2
        #             )
        #         )
        #         visited.append(city)
        #         toAdd = []
        #         for nbr in adjLists[city]:
        #             if nbr not in onScreen:
        #                 toAdd.append(mapCities[nbr])
        #                 toAdd.append(cityLabels[nbr])
        #                 toAdd.append(greyedEdges[nbr+city])
        #                 onScreen.append(nbr)
        #         # self.wait()

        #         if len(toAdd) > 0:
        #             self.play(
        #                 mapCities[city].animate.set_fill_color(visitedCityIconCenterColor),
        #                 FadeIn(*toAdd)
        #             )
        #         else:
        #             self.play(
        #                 mapCities[city].animate.set_fill_color(visitedCityIconCenterColor),
        #             )
        #     else:
        #         self.play(mapPin.animate.move_to(mapCities[city].get_center()+UP*0.1))
        
        # # self.wait()
        # self.play(
        #     LaggedStart( 
        #         mapPin.animate.move_to(mapCities[target].get_center()+UP*0.1), 
        #         Create(edges[target+city]),
        #         lag_ratio = 0.2
        #     )
        # )
        # self.play(
        #     mapCities[target].animate.
        #         set_fill_color(targetCityIconCenterColor).
        #         set_stroke_color(targetCityIconBorderColor),
        # )

        # self.wait(2)
        


        
