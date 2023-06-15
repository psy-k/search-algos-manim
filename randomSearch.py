 # #-----------------Random----------------------
        # start = 's'
        
        # mapCities[start].stroke_color = visitedCityIconBorderColor
        # mapCities[start].fill_color = visitedCityIconCenterColor
        # mapPin.move_to(mapCities[start].get_center()+UP*0.1)
        # mapPin.set_z_index(mapCities[start].z_index+1)

        # visited = [start]
        # visitOrder = ['s', 'b', 'g', 'c', 's', 'a', 'g', 'k', 'd', 'j']

        # self.wait()

        # edges['cs'] = DashedLine(
        #                 mapCities['c'].get_center(), 
        #                 mapCities['s'].get_center(), 
        #                 color=dashedEdgeColor,
        #                 stroke_width = 0.5
        #             )
        # edges['sc'] = edges['cs']
        # edges['dk'] = DashedLine(
        #                 mapCities['k'].get_center(), 
        #                 mapCities['d'].get_center(), 
        #                 color=dashedEdgeColor,
        #                 stroke_width = 0.5
        #             )
        # edges['kd'] = edges['dk']
        # edges['lf'] = DashedLine(
        #                 mapCities['l'].get_center(), 
        #                 mapCities['f'].get_center(), 
        #                 color=dashedEdgeColor,
        #                 stroke_width = 0.5
        #             )
        # edges['fl'] = edges['lf']

        # createdEdges = VGroup()
        # for i in range(1, len(visitOrder)):
        #     self.play(mapPin.animate.scale(0.5).shift(DOWN*0.05), run_time = 0.5)
        #     createdEdges.add(edges[visitOrder[i-1]+visitOrder[i]])
        #     self.play(
        #         LaggedStart(*[mapPin.animate.move_to(mapCities[visitOrder[i]].get_center()+UP*0.05), 
        #                       Create(edges[visitOrder[i-1]+visitOrder[i]])], lag_ratio=0.15))
            
        #     if visitOrder[i] not in visited:
        #         visited.append(visitOrder[i])
        #         self.play(
        #             mapPin.animate.scale(2).shift(UP*0.05), 
        #             mapCities[visitOrder[i]].animate.
        #                 set_stroke_color(visitedCityIconBorderColor).
        #                 set_fill_color(visitedCityIconCenterColor),
        #             run_time = 0.5)
        #     else:
        #         self.play(mapPin.animate.scale(2).shift(UP*0.05), run_time=0.5)
        #     self.wait()

        # self.wait()
        # removeAnims = []
        # for i in range(1, len(visited)):
        #     removeAnims.append(mapCities[visited[i]].animate.
        #         set_stroke_color(discoveredCityIconBorderColor).
        #         set_fill_color(discoveredCityIconCenterColor) 
        #     )
        # removeAnims.append(Uncreate(createdEdges))
        # removeAnims.append(mapPin.animate.move_to(mapCities[start].get_center()+UP*0.1))
        # self.play(*removeAnims)
        # self.wait(2)
