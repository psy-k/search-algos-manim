from manim import *
import random

config.background_color = "#04f404"
textColor = "#000000"

class InfoList:
    def __init__(self, cityNo, connectedCities, connectedCitiesDistances, ):
        cityBox = Rectangle(height= 3, width=2.5, color=textColor, fill_color=WHITE, fill_opacity=0.7)
        line = Line(start= LEFT*1.25+UP*0.9, end= RIGHT*1.25+UP*0.9, color=textColor)
        cityHeading = Text("City {}".format(cityNo), color=textColor).shift(UP*1.4).scale(0.6)
        cityHeading = Text("A Place".format(cityNo), color=textColor).shift(UP*1.4).scale(0.6)

        cities = []
        for i in range(len(connectedCities)):
            cities.append(Text("{}".format(connectedCities[i]), color=textColor)
                            .shift(UP*(0.65-i*0.5) + LEFT*0.8)
                            .scale(0.6))
            # if connectedCities[i] < 10:
            #     cities.append(Text("City {}".format(connectedCities[i]), color=textColor)
            #                     .shift(UP*(0.65-i*0.5) + LEFT*0.8)
            #                     .scale(0.6))
            # else:
            #     cities.append(Text("City {}".format(connectedCities[i]), color=textColor)
            #                     .shift(UP*(0.65-i*0.5) + LEFT*0.7)
            #                     .scale(0.6))
        
        cityConnectedCities = VGroup()
        for city in cities:
            cityConnectedCities.add(city)

        
        citiesDistances = []
        for i in range(len(connectedCitiesDistances)):
            citiesDistances.append(Text("{}".format(connectedCitiesDistances[i]), color=textColor)
                                   .shift(UP*(0.7-i*0.5) + RIGHT)
                                   .scale(0.6))
        cityConnectedCitiesDistances = VGroup()

        for cityDist in citiesDistances:
            cityConnectedCitiesDistances.add(cityDist)


        listBox = VGroup(cityBox, line).scale(1.2)
        list = VGroup(listBox, cityHeading, cityConnectedCities, cityConnectedCitiesDistances)


        self.listBox = listBox
        self.cityHeading = cityHeading
        self.cityConnectedCities = cityConnectedCities
        self.cityConnectedCitiesDistances = cityConnectedCitiesDistances
        self.list = list



class MapAsLists2(MovingCameraScene):
    def construct(self):
        list1 = InfoList(1, [2,3,4], [5, 10, 7])
        list1.list.shift(RIGHT*4)
        
        list2 = InfoList(2, [1,5,7], [2, 6, 3])
        list2.list.shift(RIGHT*4)

        connectedCitiesFadeIns = [FadeIn(city) for city in list1.cityConnectedCities]
        connectedCitiesDistancesFadeIns = [FadeIn(dist) for dist in list1.cityConnectedCitiesDistances]

        connectedCitiesFadeIns2 = [FadeIn(city) for city in list2.cityConnectedCities]
        connectedCitiesDistancesFadeIns2 = [FadeIn(dist) for dist in list2.cityConnectedCitiesDistances]

        
        

        # self.wait()
        # self.play(Create(list1.listBox))
        # self.wait()
        # self.play(FadeIn(list1.cityHeading))
        # self.wait()
        # self.play(LaggedStart(*connectedCitiesFadeIns, lag_ratio=0.5), duration=3)
        # self.wait()
        # self.play(LaggedStart(*connectedCitiesDistancesFadeIns))
        # self.wait()
        # self.play(FadeOut(list1.list))
        # self.wait()

        # self.play(FadeIn(list2.listBox, list2.cityHeading))
        # self.wait()
        # self.play(LaggedStart(*connectedCitiesFadeIns2, lag_ratio=0.5), duration=3)
        # self.wait()
        # self.play(LaggedStart(*connectedCitiesDistancesFadeIns2))
        # self.wait()
        # self.play(FadeOut(list2.list))
        # self.wait()
        #---------------------------------------------------------------------------------

        # miscLists = []
        # for i in range(2, 30):
        #     connectedCities = []
        #     connectedCitiesDistances = []
            
        #     noOfNeighbours = random.randint(1, 5)

        #     for j in range(noOfNeighbours):
        #         connectedCities.append(random.randint(1, 30))

        #     for j in range(noOfNeighbours):
        #         connectedCitiesDistances.append(random.randint(1, 10))

        #     miscLists.append(InfoList(i, connectedCities, connectedCitiesDistances))
        #     miscLists[i-2].list.shift(LEFT*(random.randint(-70, 70)/10) + UP*(random.randint(-40, 40)/10))
        
        # # self.add(list1.list)
        # for i in range(len(miscLists)):
        #     self.wait(1/50)
        #     if i != 0 :
        #         self.remove(miscLists[i-1].list)
        #     self.add(miscLists[i].list)
        #     self.wait(1/50)
        #---------------------------------------------------------------------------------

        
        listAPlace = InfoList(69, ["Oth", "Erc", "Iti", "Ess"], [7, 4, 6, 5])
        connectedCitiesFadeIns = [FadeIn(city) for city in listAPlace.cityConnectedCities]
        connectedCitiesDistancesFadeIns = [FadeIn(dist) for dist in listAPlace.cityConnectedCitiesDistances]

        connectedCitiesFadeIns = connectedCitiesFadeIns + connectedCitiesDistancesFadeIns

        self.wait()
        self.play(Create(listAPlace.listBox), FadeIn(listAPlace.cityHeading))
        self.wait()
        self.play(LaggedStart(*connectedCitiesFadeIns, lag_ratio=0.2),)
        # self.wait()
        # self.play(LaggedStart(*connectedCitiesDistancesFadeIns))

        self.wait()


