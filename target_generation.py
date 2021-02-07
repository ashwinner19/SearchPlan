from map_details import get_map
from random import randint


class agent_subgoal_position_generation:
    def __init__(self):
        self.map_data, self.MAP_WID, self.MAP_HEI, self.cell = get_map()
        self.start_state=[]
        self.subgoals = []
        self.number_of_subgoals_needed=5

    def initial_state(self):
        while True:
            X = randint(0, self.MAP_HEI-1) 
            Y = randint(0, self.MAP_WID-1) 
            if self.map_data[X][Y]=="false":
                self.start_state.append(X)
                self.start_state.append(Y)
                break
            else:
                continue
        return self.start_state


    def random_target(self):
        while len(self.subgoals)<self.number_of_subgoals_needed:
            X = randint(0, self.MAP_HEI-1) 
            Y = randint(0, self.MAP_WID-1) 
            print(X,Y)
            if self.map_data[X][Y]=="false" and [X,Y] not in self.subgoals:
                self.subgoals.append([X,Y])
        return self.subgoals        
