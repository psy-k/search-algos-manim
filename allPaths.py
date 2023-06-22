from manim import *
from collections import deque
from allPathsData import positions, adjLists, choices, graphColorsPlus
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


class AllPaths5(ZoomedScene):
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

        # self.add(number_plane, mapPin)

        mapCities = {}
        citiesGroup = VGroup()
        for i in range(len(positions)):
            city = i+1
            mapCities[city] = Dot(
                                radius=dotRadius, 
                                point=positions[i], 
                                color=visitedCityIconCenterColor, 
                                stroke_width=1, 
                                stroke_color=discoveredCityIconBorderColor
                            )
            # self.add(mapCities[city])
            citiesGroup.add(mapCities[city])

        
        
        edges = {}
        edgesGroup = VGroup()
        for i in range(len(positions)):
            city = i+1
            for neighbour in adjLists[i]:
                if str(city)+str(neighbour) not in edges.keys():
                    edges[str(city)+str(neighbour)] = DashedLine(
                        mapCities[city].get_center(), 
                        mapCities[neighbour].get_center(), 
                        color=dashedEdgeColor,
                        stroke_width = 0.5
                    )
                    edges[str(neighbour)+str(city)] = edges[str(city)+str(neighbour)]                    
                    mapCities[city].set_z_index(edges[str(city)+str(neighbour)].z_index+1)
                    mapCities[neighbour].set_z_index(edges[str(city)+str(neighbour)].z_index+1)

                    # self.add(edges[str(city)+str(neighbour)])
                    edgesGroup.add(edges[str(city)+str(neighbour)])

        
        x_vals_near = []
        y_vals_near = []
        pathsNear = [
            [1, 2, 3, 5],
            [1, 3, 5],
            [1, 4, 6, 3, 5],
            [1, 4, 7, 6, 3, 5],
        ]

        for path in pathsNear:
            x_vals_near.append([])
            y_vals_near.append([])
            for city in path:
                x_vals_near[-1].append(mapCities[city].get_x())
                y_vals_near[-1].append(mapCities[city].get_y())

        citiesGroup.remove(
            mapCities[1], mapCities[2], mapCities[3], 
            mapCities[4], mapCities[5], mapCities[6], 
            mapCities[7]
        )

        edgesGroup.remove(
            edges["12"], edges["13"], edges["14"], 
            edges["23"], edges["35"], edges["46"], 
            edges["36"], edges["47"], edges["67"], 
        )



        self.add(
            mapCities[1], mapCities[2], mapCities[3], 
            mapCities[4], mapCities[5], mapCities[6], 
            mapCities[7],
            
            edges["12"], edges["13"], edges["14"], 
            edges["23"], edges["35"], edges["46"], 
            edges["36"], edges["47"], edges["67"], 
        )
        mapCities[5].set_fill_color(targetCityIconCenterColor).set_stroke_color(targetCityIconBorderColor)
        mapCities[1].set_stroke_color(visitedCityIconBorderColor)
        initialTargetCopy = mapCities[5].copy()
        initialTargetCopy.set_z_index(mapCities[43].z_index+1)
        self.add(initialTargetCopy)


        self.camera.frame.scale(0.5).shift(LEFT*3+UP*0.5)

        graphsNear = []
        graphColors = [BLUE, YELLOW, GREEN, RED, PURPLE, ORANGE, TEAL, ]
        self.wait()
        shortestPathIndex = 1
        for i in range(len(pathsNear)):
            graphsNear.append(number_plane.plot_line_graph(
                x_values=x_vals_near[i], 
                y_values=y_vals_near[i],
                line_color= graphColors[i%len(graphColors)],
                add_vertex_dots= False,
                ))
            self.play(Create(graphsNear[-1]))
        self.wait()

        shortestPath = number_plane.plot_line_graph(
                x_values=x_vals_near[shortestPathIndex], 
                y_values=y_vals_near[shortestPathIndex],
                add_vertex_dots= False,
                stroke_width =20
                )
        graphsNear.append(shortestPath)
        self.play(Create(shortestPath))
        self.wait()

        
        
        newTarget = mapCities[43]
        self.wait()
        self.play(
            self.camera.frame.animate.scale(2).shift(RIGHT*3+DOWN*0.5),
            FadeIn(citiesGroup, edgesGroup), 
            FadeOut(*graphsNear),
            initialTargetCopy.animate.move_to(newTarget.get_center()).scale(2),
            mapCities[5].animate.
                set_fill_color(visitedCityIconCenterColor).
                set_stroke_color(discoveredCityIconBorderColor)
        )
        self.play(initialTargetCopy.animate.scale(0.5), run_time = 0.5)
        self.wait()

        

        # #-------------------------------All Paths----------------------------------

        start = 1
        target = 43

        paths = []

        # for i in range(100):
        #     curr = start
        #     paths.append([])
        #     while curr != target:
        #         paths[-1] += choices[curr][random.randint(0, len(choices[curr])-1)]
        #         curr = paths[-1][-1]
        
        f = open("paths5.txt", "r")
        pathsAsString = f.read()
        paths = json.loads(pathsAsString)
        # f.write(pathsAsString)
        f.close()
        
        x_vals = []
        y_vals = []
        graphs = []


        for path in paths:
            x_vals.append([])
            y_vals.append([])
            for city in path:
                x_vals[-1].append(mapCities[city].get_x())
                y_vals[-1].append(mapCities[city].get_y())

        for i in range(len(paths)):
            graphs.append(number_plane.plot_line_graph(
                x_values=x_vals[i], 
                y_values=y_vals[i],
                line_color= graphColorsPlus[i%len(graphColorsPlus)],
                add_vertex_dots= False,
                ))
            self.play(Create(graphs[-1], run_time = 0.5))
            self.add_updater(play_sequence_in_background(self, [FadeOut(graphs[-1], run_time=1)]))
        self.wait()

    





        
