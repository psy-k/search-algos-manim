from manim import *
import random, copy

config.background_color = "#04f404"
textColor = "#000000"

class InfoList:
    def __init__(self, cityNo, connectedCities, ):
        cityBox = Rectangle(height= 3, width=1.5, color=textColor, fill_color=WHITE, fill_opacity=0.7)
        line = Line(start= LEFT*0.75+UP*0.9, end= RIGHT*0.75+UP*0.9, color=textColor)
        cityHeading = Text("{}".format(cityNo), color=textColor).shift(UP*1.4).scale(0.6)

        cities = []
        for i in range(len(connectedCities)):
            cities.append(Text("{}".format(connectedCities[i]), color=textColor)
                            .shift(UP*(0.65-i*0.5) + LEFT*0.5)
                            .scale(0.6))
        
        cityConnectedCities = VGroup()
        for city in cities:
            cityConnectedCities.add(city)


        listBox = VGroup(cityBox, line).scale(1.2)
        list = VGroup(listBox, cityHeading, cityConnectedCities)


        self.listBox = listBox
        self.cityHeading = cityHeading
        self.cityConnectedCities = cityConnectedCities
        self.list = list



class SearchLists(MovingCameraScene):
    def construct(self):
        list1 = InfoList("S", ["A", "B", "C"])
        list1.list.shift(RIGHT*4)
        
        list2 = InfoList("B", ["A", "C", "D"])
        list2.list.shift(RIGHT*4)

        connectedCitiesFadeIns = [FadeIn(city) for city in list1.cityConnectedCities]

        connectedCitiesFadeIns2 = [FadeIn(city) for city in list2.cityConnectedCities]

        self.wait()
        self.play(Create(list1.listBox), FadeIn(list1.cityHeading))
        self.wait()
        self.play(LaggedStart(*connectedCitiesFadeIns, lag_ratio=0.2))
        self.wait()





        self.play(list1.list.animate.shift(LEFT*2))

        self.play(Create(list2.listBox), TransformFromCopy(list1.cityConnectedCities[1], list2.cityHeading))
        self.add(list2.cityHeading)
        
        self.play(FadeOut(list1.list))
        self.wait()
        self.play(LaggedStart(*connectedCitiesFadeIns2, lag_ratio=0.2))
        self.wait()

        list1 = InfoList("B", ["A", "C", "D"])
        list1.list.shift(RIGHT*4)
        self.play(FadeIn(list1.list), FadeOut(list2.list))
        list2 = InfoList("C", ["B", "E"])
        list2.list.shift(RIGHT*4)
        # self.add(list1.list)
        # self.remove(list2.list)
        

        connectedCitiesFadeIns = [FadeIn(city) for city in list1.cityConnectedCities]
        connectedCitiesFadeIns2 = [FadeIn(city) for city in list2.cityConnectedCities]

        self.wait(1.5)
        self.play(list1.list.animate.shift(LEFT*2))

        self.play(Create(list2.listBox), ReplacementTransform(list1.cityConnectedCities[1], list2.cityHeading))
        
        self.play(FadeOut(list1.list))
        self.wait()
        self.play(LaggedStart(*connectedCitiesFadeIns2, lag_ratio=0.2))
        self.wait()
        list1 = InfoList("C", ["B", "E"])
        self.play(FadeIn(list1.list), FadeOut(list2.list))
        # self.add(list1.list)
        # self.remove(list2.list)
        
        list2 = InfoList("D", ["E", "F"])
        
        self.wait()



