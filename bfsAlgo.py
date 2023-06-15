        # #-----------BFS----------------
        # # what a shame lmao
        # start = 's'
        # target = 't'
        
        # mapCities[start].stroke_color = visitedCityIconBorderColor
        # mapCities[start].fill_color = visitedCityIconCenterColor

        # mapCities[target].stroke_color = targetCityIconBorderColor
        # mapCities[target].fill_color = targetCityIconCenterColor

        # visited = []
        # discovered = deque()
        # curr = start

        # prev = []
        # discovered += adjLists[curr]
        # visited.append(curr)
        # mapPin.set_z_index(mapCities['q'].z_index + 1)
        # mapPin.move_to(mapCities[start].get_center()+UP*0.1)




        
        # self.wait()

        # parent = {}
        # parent['s'] = None

        # pinScale = 1
        # offset = UP*0.05

        # visitOrder = ['s', 'a', 's', 'b', 's', 'c', 's', 'a', 'h', 'a', 'e', 't']
        

        # for i in range(1, len(visitOrder)):
        #     if visitOrder[i] not in visited:
        #         visited.append(visitOrder[i])
        #         if pinScale == 1:
        #             self.play(mapPin.animate.scale(0.5), run_time = 0.5)
        #         else:
        #             pinScale = 1

        #         self.play(LaggedStart( *[mapPin.animate.move_to(mapCities[visitOrder[i]].get_center()+offset), 
        #                                     Create(edges[visitOrder[i-1]+visitOrder[i]])] 
        #                                 ,lag_ratio=0.2))
        #         self.play(
        #             mapPin.animate.scale(2).shift(UP*0.05), 
        #             mapCities[visitOrder[i]].
        #                 animate.set_stroke_color(visitedCityIconBorderColor).
        #                 set_fill_color(visitedCityIconCenterColor),
        #             run_time = 0.5
        #         )
        #         self.wait()
        #     else:
        #         if pinScale == 1:
        #             self.play(mapPin.animate.scale(0.5), run_time = 0.5)
        #             pinScale = 0.5

        #         self.play(mapPin.animate.move_to(mapCities[visitOrder[i]].get_center()+offset))
        #         # self.wait()

        # self.wait(2)
        # finalPathColor =  BLUE #"#4ca95e" # "#ffd633" # "#fe4e00" # "#e9190f" # "#09a129" # "#f08700" # "#499f68" 
        # prev = ['s', 'a', 'e']
        # finalPath = []
        # for i in range(1, len(prev)):
        #     finalPath.append(
        #         Line(
        #             start = mapCities[prev[i-1]].get_center(),
        #             end = mapCities[prev[i]].get_center(),
        #             color = finalPathColor,
        #             stroke_width = 16,
        #         )
        #     )
            
        #     finalPath[i-1].set_z_index(mapCities[prev[i-1]].z_index+1)
        #     finalPath[i-1].set_opacity(0.5).scale(1.2)
            
        #     self.play(Create(finalPath[i-1]))

        # finalPath.append(
        #         Line(
        #             start = mapCities[prev[-1]].get_center(),
        #             end = mapCities[target].get_center(),
        #             color = finalPathColor,
        #             stroke_width = 16,
        #         )
        #     )
            
        # finalPath[-1].set_z_index(mapCities[prev[i-1]].z_index+1)
        # finalPath[-1].set_opacity(0.5).scale(1.2)
        # mapPin.set_z_index(finalPath[-1].z_index+1)
        
        # self.play(Create(finalPath[-1]))
        # self.wait(2)