from manim import *

class DataList:
    def __init__(self, cityNo, connectedCities, connectedCitiesDistances, textColor=BLACK):
        textScale = 0.6
        cityBox = Rectangle(height= 2.5, width=2.0, color=textColor, fill_color=WHITE, fill_opacity=0.7, stroke_width = 2.5)
        line = Line(start= LEFT*1.+UP*0.8, end= RIGHT*1.+UP*0.8, color=textColor, stroke_width = 2.5)
        cityHeading = Text("{}".format(cityNo), color=textColor).shift(UP*1.25).scale(textScale)

        cities = []
        for i in range(len(connectedCities)):
            cities.append(Text("{}".format(connectedCities[i].upper()), color=textColor)
                            .shift(UP*(0.62-i*0.5) + LEFT*0.6)
                            .scale(textScale))        
        cityConnectedCities = VGroup()
        for city in cities:
            cityConnectedCities.add(city)

        
        citiesDistances = []
        for i in range(len(connectedCitiesDistances)):
            citiesDistances.append(Text("{}".format(connectedCitiesDistances[i]), color=textColor)
                                   .shift(UP*(0.62-i*0.5) + RIGHT*0.7)
                                   .scale(textScale))
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


listPositions = []
