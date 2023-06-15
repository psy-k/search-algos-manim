        # #-----------DFS----------------
        # start = 's'
        # target = 't'
        
        # mapCities[start].stroke_color = visitedCityIconBorderColor
        # mapCities[start].fill_color = visitedCityIconCenterColor

        # mapCities[target].stroke_color = targetCityIconBorderColor
        # mapCities[target].fill_color = targetCityIconCenterColor

        # visited = []
        # curr = start
        # prev = []
        # visited.append(curr)
        # mapPin.set_z_index(mapCities['q'].z_index + 1)
        # mapPin.move_to(mapCities[start].get_center()+UP*0.1)




        
        # self.wait(3)

        # pinScale = 1
        # offset = UP*0.07
        # while curr is not target:
        #     flag = 0
        #     for neighbour in adjLists[curr]:
        #         if neighbour not in visited:
        #             if pinScale == 1:
        #                 self.play(mapPin.animate.scale(0.8).shift(DOWN*0.03), run_time = 0.5)
        #                 self.play(LaggedStart( *[mapPin.animate.move_to(mapCities[neighbour].get_center()+offset), 
        #                                         Create(edges[curr+neighbour])] 
        #                                     ,lag_ratio=0.15))
        #                 pinScale = 0.5
        #             else:
        #                 self.play(LaggedStart( *[mapPin.animate.move_to(mapCities[neighbour].get_center()+offset), 
        #                                         Create(edges[curr+neighbour])] 
        #                                     ,lag_ratio=0.15))
                        
                    

        #             if neighbour is not target:
        #                 self.play(
        #                     # mapPin.animate.scale(2).shift(UP*0.05), 
        #                     # mapCities[neighbour].animate.set_stroke_color(visitedCityIconBorderColor),
        #                     mapCities[neighbour].animate.set_fill_color(visitedCityIconCenterColor),
        #                     run_time = 0.5
        #                 )
        #             else:
        #                 self.play(
        #                     mapPin.animate.scale(1/0.8).shift(UP*0.03), 
        #                     # mapCities[neighbour].animate.set_stroke_color(visitedCityIconBorderColor),
        #                     # mapCities[neighbour].animate.set_fill_color(visitedCityIconCenterColor),
        #                     run_time = 0.5
        #                 )
        #             # self.wait()
        #             prev.append(curr)
        #             curr = neighbour
        #             visited.append(curr)
        #             flag = 1
        #             break

        #     if flag == 0:
                
        #         if pinScale == 1:
        #             self.play(mapPin.animate().scale(0.5).move_to(mapCities[curr].get_center()+offset))
        #             pinScale = 0.5
        #         curr = prev.pop()
        #         self.play(mapPin.animate.move_to(mapCities[curr].get_center()+offset))
        #         # self.wait()



        # self.wait(2)
        # finalPathColor =  BLUE #"#4ca95e" # "#ffd633" # "#fe4e00" # "#e9190f" # "#09a129" # "#f08700" # "#499f68" 
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
