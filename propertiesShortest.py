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


class ShortestPathProperties3(ZoomedScene):
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
            self.add(mapCities[city])

        
        
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

                    self.add(edges[str(city)+str(neighbour)])

        
        mapCities[43].set_fill_color(targetCityIconCenterColor).set_stroke_color(targetCityIconBorderColor)
        mapCities[1].set_stroke_color(visitedCityIconBorderColor)

        x_vals = []
        y_vals = []
        paths = [
            [14, 18, 22, 28, 34, 39, 43],
            [1, 4, 6, 8, 10, 11, 14, 18, 22, 28, 34, 39, 43],
            [1, 3, 5, 14],
            [1, 3, 5, 14], 
            [14, 18, 22, 28, 34, 39, 43],
        ]
        graphs = []

        initialShortestPath = 1
        initialShortestPath2 = 0
        shorterSubPath = 2
        actualShortestPath1 = 3
        actualShortestPath2 = 4


        graphColors = [BLUE, BLUE, GREEN, RED, RED]


        
        for path in paths:
            x_vals.append([])
            y_vals.append([])
            for city in path:
                x_vals[-1].append(mapCities[city].get_x())
                y_vals[-1].append(mapCities[city].get_y())

        for i in range(len(paths)):
            graphs.append(
                number_plane.plot_line_graph(
                x_values=x_vals[i], 
                y_values=y_vals[i],
                add_vertex_dots= False,
                line_color = graphColors[i],
                stroke_width = 7 if i == actualShortestPath1 or i == actualShortestPath2 else 5
            )
        )
            
        labels = []
        labelDots = []
        labelLines = []
        labelTexts = []
        textData = [
            "Shortest path (Alleged)",
            "Shorter path to C",
            "Actual Shortest path ",
        ]

        for i in range(1, len(paths)-1):
            labelDots.append(
                Dot(
                    LEFT*6.7+UP*(3.2-0.5*(i-1)),
                    radius=0.08,
                    color=graphColors[i],
                    stroke_width=0
                )
            )
            labelDots.append(
                Dot(
                    LEFT*6.4+UP*(3.2-0.5*(i-1)),
                    radius=0.08,
                    color=graphColors[i],
                    stroke_width=0
                )
            )
            labelLines.append(
                Line(
                    labelDots[-2].get_center(),
                    labelDots[-1].get_center(),
                    color=graphColors[i],
                    stroke_width =  5,
                )
            )
            labelTexts.append(
                Tex(
                    textData[i-1],
                    color=BLACK,
                ).scale(0.5).next_to(labelDots[-1], RIGHT)
            )
            labels.append(
                VGroup(labelDots[-2], labelDots[-1], labelLines[-1], labelTexts[-1])
            )

        startLabel = Tex("S", color = BLACK).scale(0.5).move_to(mapCities[1].get_center()+LEFT*0.2)
        targetLabel = Tex("T", color = BLACK).scale(0.5).move_to(mapCities[43].get_center()+RIGHT*0.2)
        cityLabel = Tex("C", color = BLACK).scale(0.5).move_to(mapCities[14].get_center()+RIGHT*0.15+DOWN*0.15)
        start = 1
        target = 43


        # self.wait()
        # self.play(
        #     GrowFromCenter(
        #         startLabel, 
        #         rate_func = rate_functions.ease_in_out_back,
        #         run_time = 0.5
        #     ),
        # )
        # self.play( 
        #     Create(graphs[initialShortestPath]),
        # )
        # self.play(
        #     GrowFromCenter(
        #         targetLabel, 
        #         rate_func = rate_functions.ease_in_out_back,
        #         run_time = 0.5
        #     ), 
        # )
        # labels[initialShortestPath-1].shift(DOWN*0.25).set_opacity(0)
        # self.play(labels[initialShortestPath-1].animate.shift(UP*0.25).set_opacity(1))
        # self.add(graphs[initialShortestPath2])
        # self.wait()

        # cityAnims = []
        # for city in paths[initialShortestPath]:
        #     if (city is not start) and (city is not target):
        #         cityAnims.append(
        #             ScaleInPlace(mapCities[city], 2, rate_func = rate_functions.there_and_back)
        #         )
        
        # self.wait()
        # self.play(LaggedStart(*cityAnims, run_time = 2))
        # self.wait(2)
        # self.play(ScaleInPlace(mapCities[target], 2), rate_func = rate_functions.ease_in_out_back)
        # self.wait()

        # cityAnims = []
        # for city in paths[initialShortestPath]:
        #     if (city is not start) and (city is not target):
        #         cityAnims.append(
        #             ScaleInPlace(mapCities[city], 2, rate_func = rate_functions.ease_in_out_back)
        #         )
        # self.wait()
        # self.play(LaggedStart(*cityAnims, run_time = 2))
        # self.wait(2)

        # self.play(Create(graphs[shorterSubPath]))
        # self.play(GrowFromCenter(
        #                 cityLabel, 
        #                 rate_func = rate_functions.ease_in_out_back,
        #                 run_time = 0.7
        #             )
        #         )
        # labels[shorterSubPath-1].shift(DOWN*0.25).set_opacity(0)
        # self.play(labels[shorterSubPath-1].animate.shift(UP*0.25).set_opacity(1))
        # self.wait(2) 

        # self.play(Create(graphs[actualShortestPath1]), graphs[shorterSubPath].animate.shift(DOWN*0.05))
        # self.wait()
        # self.play(Create(graphs[actualShortestPath2]), graphs[initialShortestPath2].animate.shift(DOWN*0.05))
        
        # labels[actualShortestPath1-1].shift(DOWN*0.25).set_opacity(0)
        # self.play(labels[actualShortestPath1-1].animate.shift(UP*0.25).set_opacity(1))
        # self.wait(3)


        # cityAnims = []
        # for city in paths[initialShortestPath]:
        #     if (city is not start):
        #         cityAnims.append(
        #             ScaleInPlace(mapCities[city], 0.5)
        #         )

        # allResetAnims = [
        #     FadeOut(
        #         graphs[initialShortestPath], graphs[shorterSubPath], 
        #         graphs[actualShortestPath1], graphs[actualShortestPath2],
        #         graphs[initialShortestPath2],
        #         labels[initialShortestPath-1], labels[shorterSubPath-1], labels[actualShortestPath1-1],
        #         cityLabel,
        #     ),
        # ] + cityAnims
        # self.play(*allResetAnims) 
        # self.wait(2)


        self.add(startLabel, targetLabel)
        qMarks = []
        qMarkAnims = []
        for city in range(2, 52):
            if city != 43:
                qMarks.append(Tex("?", color = DARK_GRAY).scale(0.6).move_to(mapCities[city].get_center()+UP*0.1))
                qMarks[-1].set_z_index(mapCities[51].z_index + 1)
                qMarkAnims.append(GrowFromCenter(qMarks[-1], rate_func = rate_functions.ease_in_out_back))
        
        self.play(LaggedStart(*qMarkAnims, run_time = 2),)
        self.wait(2)

        tickMarks = []
        tickMarkAnims = []
        for city in range(2, 52):
            if city != 43:
                tickMarks.append(Tex("\\checkmark", color = GREEN).scale(0.6).move_to(mapCities[city].get_center()+UP*0.1+RIGHT*0.05))
                tickMarks[-1].set_z_index(mapCities[51].z_index + 1)
        
        for i in range(len(qMarks)):
            tickMarkAnims.append(ReplacementTransform(qMarks[i], tickMarks[i], rate_func = rate_functions.ease_in_out_back))
        
        self.play(LaggedStart(*tickMarkAnims, run_time = 2),)
        self.wait(2)









        
