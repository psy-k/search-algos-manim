from manim import *
import random

# config.background_color = "#04f404"
textColor = "#000000"
textScale = 0.25
listLimit = 7
ZOOM = "zoom"
FADEIN = "fadein"

class ListCity:
    def __init__(self, name, parent, distance):
        self.name = name
        self.parent = parent
        self.distance = distance


class InfoList:
    def __init__(self, title, cities, offset):
        self.title = title
        self.cities = cities
        self.offset = offset

        listBox = Rectangle(
            height= 2.5, width=1.7, 
            color=textColor, 
            fill_color=WHITE, fill_opacity=0.7, 
            stroke_width = 1.5
        ).shift(offset)
        line = Line(start= LEFT*0.85+UP*0.9, end= RIGHT*0.85+UP*0.9, color=textColor, stroke_width = 1.5).shift(offset)
        heading = Text(title, color=textColor).scale(textScale).shift(UP*1.07+offset)
        box = VGroup(listBox, heading, line)
        ellipses1 = Text(".", color=textColor).scale(textScale).shift(UP*0.75 + offset)
        ellipses2 = Text(".", color=textColor).scale(textScale).move_to(ellipses1.get_center()+DOWN*0.05)
        ellipses3 = Text(".", color=textColor).scale(textScale).move_to(ellipses2.get_center()+DOWN*0.05)
        ellipses = VGroup(ellipses1, ellipses2, ellipses3)
        

        cityNameMobjects = []
        cityDistanceMobjects = []
        cityParentMobjects = []
        cityVGroups2 = []
        cityVGroups3 = []
        for i in range(len(cities)):
            cityNameMobjects.append(Text(cities[i].name, color=textColor)
                                    .scale(textScale)
                                    .shift(UP*(0.70-i*0.3) + LEFT*0.5 + offset)
                                )
            cityDistanceMobjects.append(Text(str(cities[i].distance), color=textColor)
                                        .scale(textScale)
                                        .shift(UP*(0.70-i*0.3) + RIGHT*0.5 + offset)
                                    )
            cityParentMobjects.append(Text(cities[i].parent, color=textColor)
                                        .scale(textScale)
                                        .shift(UP*(0.70-i*0.3) + RIGHT*1.4 + offset)
                                    )
            
            cityVGroups2.append(
                VGroup(
                cityNameMobjects[-1],
                cityDistanceMobjects[-1],
                )
            )
            cityVGroups3.append(
                VGroup(
                cityNameMobjects[-1],
                cityDistanceMobjects[-1],
                cityParentMobjects[-1],
                )
            )
        

        self.box = box
        self.heading = heading
        self.ellipses = ellipses
        self.cityNameMobjects = cityNameMobjects
        self.cityDistanceMobjects = cityDistanceMobjects
        self.cityParentMobjects = cityParentMobjects
        self.cityVGroups2 = cityVGroups2
        self.cityVGroups3 = cityVGroups3


    def getDistMobject(self, city):
        for i in range(self.cities):
            if self.cities[i].name == city:
                return self.cityDistanceMobjects[i]
            

    def showDistanceAsSum(self, cityIndex, baseDist, finalEdgeDist, newParent, baseWtMobject, edgeWtMobject, onNewCityAdded = False):
        newDistance = baseDist + finalEdgeDist
        oldDistance = self.cities[cityIndex].distance
        cityNameMobject = self.cityNameMobjects[cityIndex]
        cityDistanceMobject = self.cityDistanceMobjects[cityIndex]
        
        if onNewCityAdded:
            upShift = UP*0.3
            rightShift = RIGHT*0.8
        else:
            upShift = UP*0
            rightShift = RIGHT*0.6
                
        addnBase = Text(str(baseDist), color=textColor
                    ).scale(textScale)
        addnSign = Text("+", color=textColor
                    ).scale(textScale).next_to(addnBase, RIGHT).shift(LEFT*0.2)
        addnFinalEdge = Text(
                            str(finalEdgeDist), 
                            color=textColor
                        ).scale(textScale).next_to(addnSign, RIGHT).shift(LEFT*0.2)
        
        newDistanceAsSum = VGroup(addnBase, addnSign, addnFinalEdge)

        if onNewCityAdded:
            newDistanceAsSum.move_to(cityDistanceMobject.get_center())
        else:
            newDistanceAsSum.move_to(cityNameMobject.get_center() + RIGHT*0.55 + upShift)

        
        if newDistance < oldDistance:
            compareSignText = "<"
            compareSignColor = PURE_GREEN
        elif newDistance == oldDistance:
            compareSignText = "="
            compareSignColor = textColor
        else:
            compareSignText = ">"
            compareSignColor = textColor

        compareSign = Text(
                            compareSignText, 
                            color=compareSignColor
                        ).scale(textScale).next_to(addnFinalEdge, RIGHT).shift(LEFT*0.23)
        

        if onNewCityAdded:
            tempNewDist = Text(
                                str(newDistance), 
                                color=textColor
                            ).scale(textScale).move_to(cityDistanceMobject.get_center())
        else:
            tempNewDist = Text(
                                str(newDistance), 
                                color=textColor
                            ).scale(textScale).move_to(cityNameMobject.get_center() + RIGHT*0.65 + upShift)
        
        anims = [
                    TransformFromCopy(baseWtMobject, addnBase),
                    GrowFromCenter(addnSign),
                    TransformFromCopy(edgeWtMobject, addnFinalEdge),
                    None,
                    ReplacementTransform(newDistanceAsSum, tempNewDist),
                ]
        
        if not onNewCityAdded:
            anims += [
                FadeIn(compareSign),
                None,
            ]
        
        if compareSignText == "<":
            self.cities[cityIndex].distance = newDistance
            self.cities[cityIndex].parent = newParent
            self.cityDistanceMobjects[cityIndex] = tempNewDist
            self.cityVGroups2[cityIndex] = VGroup(
                self.cityNameMobjects[cityIndex],
                self.cityDistanceMobjects[cityIndex],
            )
            self.cityVGroups3[cityIndex] = VGroup(
                self.cityNameMobjects[cityIndex],
                self.cityDistanceMobjects[cityIndex],
                self.cityParentMobjects[cityIndex]
            )
            anims += [FadeOut(compareSign), self.cityDistanceMobjects[cityIndex].animate.shift(RIGHT*0.35)]
        else:
            if onNewCityAdded:
                anims += [FadeOut(tempNewDist), None]
            else:
                anims += [FadeOut(compareSign, tempNewDist), None]
                
        
        return anims
                

    def addCity(self, index, animType, cityLabels, fadeInTogether = False):
        newCity = self.cities[index]
        totalCities = len(self.cities)

        onScreenIndex = 0

        if totalCities < 7:
            onScreenIndex = index
        elif totalCities >= 7:
            onScreenIndex = 5

        self.cityNameMobjects.append(Text(newCity.name, color=textColor)
                                        .scale(textScale)
                                        .shift(UP*(0.70-onScreenIndex*0.3) + LEFT*0.5 + self.offset)
                                    )
        self.cityDistanceMobjects.append(Text(str(newCity.distance), color=textColor)
                                        .scale(textScale)
                                        .shift(UP*(0.70-onScreenIndex*0.3) + RIGHT*0.5 + self.offset)
                                    )
        self.cityParentMobjects.append(Text(newCity.parent, color=textColor)
                                        .scale(textScale)
                                        .shift(UP*(0.70-onScreenIndex*0.3) + RIGHT*1.0 + self.offset)
                                    )
        
        self.cityVGroups2.append(
            VGroup(
                self.cityNameMobjects[-1],
                self.cityDistanceMobjects[-1],
            )
        )
        self.cityVGroups3.append(
            VGroup(
                self.cityNameMobjects[-1],
                self.cityDistanceMobjects[-1],
                self.cityParentMobjects[-1],
            )
        )        
        
        if animType == FADEIN:
            if fadeInTogether == True:
                self.cityVGroups2[-1].shift(DOWN*0.3).set_opacity(0)
                return [
                self.cityVGroups2[-1].animate.shift(UP*0.3).set_opacity(1),
            ]
            else:
                return [
                    TransformFromCopy(cityLabels[newCity.name.lower()], self.cityNameMobjects[-1]),
                    # self.cityNameMobjects[-1].animate.shift(UP*0.3).set_opacity(1),
                    self.cityDistanceMobjects[-1].animate.set_opacity(1)
                ]
        else:
            return [AnimationGroup(
                GrowFromCenter(self.cityNameMobjects[-1]),
                GrowFromCenter(self.cityDistanceMobjects[-1]),
            )]
        
        
    def updateDistance(self, cityName, newDistBase, newDistFinalEdge, newParent, cityLabelMobject, baseWtMobject, edgeWtMobject):
        for i in range(len(self.cities)):
            if self.cities[i].name == cityName:
                
                oldDistanceMobject = self.cityDistanceMobjects[i]
                nameMobjectCopy = self.cityNameMobjects[i].copy()

                
                anims = [
                    TransformFromCopy(cityLabelMobject, nameMobjectCopy),
                    FadeOut(nameMobjectCopy, run_time = 0)
                ]
                distAsSumAnims = self.showDistanceAsSum(
                    i, 
                    newDistBase, 
                    newDistFinalEdge, 
                    newParent, 
                    baseWtMobject, 
                    edgeWtMobject
                )

                anims += distAsSumAnims[:-2]

                if distAsSumAnims[-1] == None:
                    anims.append(distAsSumAnims[-2])
                else:
                    anims.append(AnimationGroup(FadeOut(oldDistanceMobject), distAsSumAnims[-2]))
                anims.append(distAsSumAnims[-1])

                return anims
            
    def swap(self, myList, i, j):
        temp = myList[i]
        myList[i] = myList[j]
        myList[j] = temp 

    def sortList(self):
        order = [i for i in range(len(self.cities))]
        
        for i in range(len(self.cities)):
            for j in range(len(self.cities)-1):
                if self.cities[j].distance > self.cities[j+1].distance:
                    self.swap(self.cities, j, j+1)
                    self.swap(self.cityDistanceMobjects, j, j+1)
                    self.swap(self.cityNameMobjects, j, j+1)
                    self.swap(self.cityParentMobjects, j, j+1)
                    self.swap(self.cityVGroups2, j, j+1)
                    self.swap(self.cityVGroups3, j, j+1)
                    self.swap(order, j, j+1)
        
        anims = [
            AnimationGroup(
                *[self.cityVGroups2[i].animate.shift(DOWN*(i-order[i])*0.3) for i in range(len(self.cities))]
            )
        ]

        return anims
                    


    def removeFirstEntry(self):
        
        removedListEntry = self.cityVGroups2[0]
        
        self.cities.pop(0)
        self.cityVGroups2.remove(removedListEntry)
        self.cityVGroups3.remove(self.cityVGroups3[0])
        removedCityName = self.cityNameMobjects.pop(0)
        removedCityDist = self.cityDistanceMobjects.pop(0)
        removedCityParent = self.cityParentMobjects.pop(0)

        shiftUps = []
        for group in self.cityVGroups2:
            shiftUps.append(group.animate.shift(UP*0.3))

        anims = [
            AnimationGroup(
                ShrinkToCenter(removedCityName), 
                ShrinkToCenter(removedCityDist)
            ),
            # None,
            LaggedStart(*shiftUps),
            # None,
        ]
        return anims
    

    def addCities(self, cities, animType, cityLabels, fadeInTogether = False):
        initialNoOfCities = len(self.cities)
        finalNoOfCities = len(self.cities) + len(cities)

        self.cities += cities
        anims = []

        if finalNoOfCities >= 7:
            groupAnims = []
            if finalNoOfCities == 7:
                groupAnims.append(
                    AnimationGroup(
                        FadeIn(self.ellipses),
                        FadeOut(self.cityVGroups2[0])
                    )
                )

            groupAnims += [self.cityVGroups2[finalNoOfCities-6].animate.shift(UP*0.3).set_opacity(0)]
            groupAnims += [self.cityVGroups2[i].animate.shift(UP*0.3) for i in range(finalNoOfCities-5, finalNoOfCities-1)]
            anims += [
                LaggedStart(*groupAnims),
                # None,
            ]

        i = initialNoOfCities
        for city in cities:
            anims += self.addCity(i, animType, cityLabels, fadeInTogether=fadeInTogether)
            i += 1

        return anims
    
