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

class DijkstrasIntroP1(ZoomedScene):

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

        mapCities['t'].set_fill_color(targetCityIconCenterColor)
        mapCities['t'].set_stroke_color(targetCityIconBorderColor)

        mapPin.set_z_index(mapCities['t'].z_index + 1)

        mapPin.move_to(mapCities['s'].get_center() + UP*0.1)
        
        visitedCity = 's'
        target = 't'

        cityNamesMobjects = {
            's' : Text("S", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-1*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'a' : Text("A", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-2*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'b' : Text("B", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-3*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'c' : Text("C", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-4*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'd' : Text("D", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-5*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'e' : Text("E", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-6*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
            'f' : Text("F", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-7*0.3) + LEFT*0.5 + discoveredOffset)
                        .set_opacity(0),
        }
        
        cityDistanceMobjects = {
            's' : Text("0", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-0*0.3) + RIGHT*0.5 + visitedOffset),
                        # .set_opacity(0),
            'a' : Text("3", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-1*0.3) + RIGHT*0.5 + visitedOffset),
                        # .set_opacity(0),
            'b' : Text("2", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-2*0.3) + RIGHT*0.5 + visitedOffset),
                        # .set_opacity(0),
            'c' : Text("7", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-0*0.3) + RIGHT*0.5 + discoveredOffset),
                        # .set_opacity(0),
            'd' : Text("8", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-1*0.3) + RIGHT*0.5 + discoveredOffset),
                        # .set_opacity(0),
            'e' : Text("7", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-2*0.3) + RIGHT*0.5 + discoveredOffset),
                        # .set_opacity(0),
            'f' : Text("11", color=textColor)
                        .scale(textScale)
                        .shift(UP*(0.70-3*0.3) + RIGHT*0.5 + discoveredOffset),
                        # .set_opacity(0),
        }


        addCititesAnims = [
            AnimationGroup(GrowFromCenter(mapCities["s"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["s"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["a"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["a"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["b"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["b"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["c"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["c"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["d"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["d"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["e"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["e"], rate_func= rate_functions.ease_out_back)),
            AnimationGroup(GrowFromCenter(mapCities["f"], rate_func= rate_functions.ease_out_back),
                           GrowFromCenter(cityLabels["f"], rate_func= rate_functions.ease_out_back)),
        ]
        createEdgesAnims = [
            Create(greyedEdges['sa']),
            Create(greyedEdges['sb']),
            Create(greyedEdges['ab']),
            Create(greyedEdges['bc']),
            Create(greyedEdges['bd']),
            Create(greyedEdges['ae']),
            Create(greyedEdges['af']),
        ]

        addCitiesToListAnims = [
            cityNamesMobjects['s'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['a'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['b'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['c'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['d'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['e'].animate.shift(UP*0.3).set_opacity(1),
            cityNamesMobjects['f'].animate.shift(UP*0.3).set_opacity(1),
        ]

        self.wait(2)

        visitedList.heading.set_opacity(0)
        discoveredList.heading.set_opacity(0)

        self.play(
            LaggedStart(
                GrowFromCenter(visitedList.box, rate_func= rate_functions.ease_out_back),
                GrowFromCenter(discoveredList.box, rate_func= rate_functions.ease_out_back),
            )
        )

        self.remove(visitedList.heading, discoveredList.heading)
        visitedList.heading.set_opacity(1)
        discoveredList.heading.set_opacity(1)

        self.play(Write(discoveredList.heading))
        self.wait()
        

        self.play(
            LaggedStart(
                LaggedStart(*addCititesAnims, lag_ratio=0.15), 
                AnimationGroup(*createEdgesAnims),
                lag_ratio = 0.3
            ),
            LaggedStart(
                *addCitiesToListAnims,
                lag_ratio = 0.15
            )
        )

        
        self.wait()
        self.play(Write(visitedList.heading))
        self.wait()
        self.play(
            LaggedStart(
                AnimationGroup(
                    mapCities['s'].animate.set_fill_color(visitedCityIconCenterColor),
                    mapCities['a'].animate.set_fill_color(visitedCityIconCenterColor),
                    mapCities['b'].animate.set_fill_color(visitedCityIconCenterColor),
                ),
                FadeIn(mapPin),
                LaggedStart(
                    Create(edges['sb']),
                    Create(edges['ba']),
                    lag_ratio = 0.3
                ),
                lag_ratio = 0.2
            ),
            LaggedStart(
                LaggedStart(
                    AnimationGroup(
                            cityNamesMobjects['s'].animate.shift(UP*2.75),
                            rate_func = rate_functions.ease_in_out_back,
                    ),
                    cityNamesMobjects['a'].animate.shift(UP*2.75),
                    cityNamesMobjects['b'].animate.shift(UP*2.75),
                    lag_ratio = 0.15
                ),
                LaggedStart(
                    cityNamesMobjects['c'].animate.shift(UP*0.9),
                    cityNamesMobjects['d'].animate.shift(UP*0.9),
                    cityNamesMobjects['e'].animate.shift(UP*0.9),
                    cityNamesMobjects['f'].animate.shift(UP*0.9),
                    lag_ratio = 0.15
                ),
                lag_ratio = 0.5
            )
        )

        self.wait()

        self.play(
            # AnimationGroup(
                LaggedStart(
                    GrowFromCenter( weights['sb'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( weights['ba'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['sb'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['ba'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['sa'],rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['bc'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['bd'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['ae'], rate_func = rate_functions.ease_out_back,),
                    GrowFromCenter( greyedWeights['af'], rate_func = rate_functions.ease_out_back,),
                ),
            # ),
            LaggedStart(
                FadeIn(cityDistanceMobjects['s']),
                FadeIn(cityDistanceMobjects['a']),
                FadeIn(cityDistanceMobjects['b']),
                FadeIn(cityDistanceMobjects['c']),
                FadeIn(cityDistanceMobjects['d']),
                FadeIn(cityDistanceMobjects['e']),
                FadeIn(cityDistanceMobjects['f']),
                lag_ratio = 0.2
            )
        )
        self.wait()

        self.play(mapPin.animate.move_to(mapCities['b'].get_center() + UP*0.1))
        self.play(
            LaggedStart(
                mapPin.animate.move_to(mapCities['c'].get_center() + UP*0.1),
                Create(edges['bc']),
                FadeIn(weights['bc']),
                lag_ratio = 0.2
            )
        )
        self.play(
            mapCities['c'].animate.set_fill_color(visitedCityIconCenterColor)
        )
        self.wait()

        self.play(
            ShrinkToCenter(cityNamesMobjects['c'], rate_func = rate_functions.ease_in_back), 
            ShrinkToCenter(cityDistanceMobjects['c'], rate_func = rate_functions.ease_in_back)
        )
        cityNamesMobjects['c'] = Text("C", color=textColor).scale(textScale).shift(UP*(0.70-3*0.3) + LEFT*0.5 + visitedOffset)
        cityDistanceMobjects['c'] = Text("7", color=textColor).scale(textScale).shift(UP*(0.70-3*0.3) + RIGHT*0.5 + visitedOffset)
        self.play(
            GrowFromCenter(cityNamesMobjects['c'], rate_func = rate_functions.ease_out_back), 
            GrowFromCenter(cityDistanceMobjects['c'], rate_func = rate_functions.ease_out_back)
        )
        self.play(
            LaggedStart(
                AnimationGroup(
                    cityNamesMobjects['d'].animate.shift(UP*0.3),
                    cityDistanceMobjects['d'].animate.shift(UP*0.3),
                ),
                AnimationGroup(
                    cityNamesMobjects['e'].animate.shift(UP*0.3),
                    cityDistanceMobjects['e'].animate.shift(UP*0.3),
                ),
                AnimationGroup(
                    cityNamesMobjects['f'].animate.shift(UP*0.3),
                    cityDistanceMobjects['f'].animate.shift(UP*0.3),
                ),
            )
        )
        self.wait()

        prev = ['s', 'b', 'c']
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
        
        # self.wait()
        shortestPathText = Paragraph(
            "Shortest Path",
            "to C",
            "FOR SURE", 
            color = BLUE,
            alignment = "center",
        ).scale(0.2).move_to(mapCities['b'].get_center() + LEFT*0.75 + DOWN*0.25)
        
        self.play(FadeIn(shortestPathText[:2]))
        self.wait()
        self.play(FadeIn(shortestPathText[2]))
        self.wait()

        self.wait(2)
        clearAnims = [
            Uncreate(finalPath[0]),
            Uncreate(finalPath[1]),
            mapPin.animate.move_to(mapCities['s'].get_center() + UP*0.1),
            Uncreate(edges['sb']),
            Uncreate(edges['bc']),
            Uncreate(edges['ba']),
            Uncreate(weights['sb']),
            Uncreate(weights['bc']),
            Uncreate(weights['ba']),
            mapCities['b'].animate.set_fill_color(discoveredCityIconCenterColor),
            mapCities['a'].animate.set_fill_color(discoveredCityIconCenterColor),
            mapCities['c'].animate.set_fill_color(discoveredCityIconCenterColor),
            FadeOut(shortestPathText)
        ]

        self.play(*clearAnims)
        self.wait()

        self.play(
            LaggedStart(
                GrowFromCenter(mapCities['j'], rate_func = rate_functions.ease_out_back),
                GrowFromCenter(mapCities['j'], rate_func = rate_functions.ease_out_back),
            )
        )
        
        self.wait(2)