import random
import numpy as np
import math
import pygame
import constants
from reward import reward
from map_details import get_map


# Define the Player
class Player():
    def __init__(self):
        super(Player, self).__init__()
        self.actions = ["left","right","up","down"]
        self.state_lb = [0,0]
        self.state_ub = [49,49]
        self.display = False
        self.goal_reached = False
        self.display = False
        self.map_dat,self.MAP_WID,self.MAP_HEI,self.cell = get_map()

    # Move the sprite based on keypresses
    def move(self,position,action,subgoal_count,t):
        if action == "left":
            xp = [position[0] - 1,position[1]]
        elif action == "right":
            xp = [position[0] + 1,position[1]]
        elif action == "up":
            xp = [position[0],position[1] - 1]
        elif action == "down":
            xp = [position[0],position[1] + 1]

       
        xp[0] = min(max(xp[0],self.state_lb[0]),self.state_ub[0])
        xp[1] = min(max(xp[1],self.state_lb[1]),self.state_ub[1])
        
        #if self.map_dat[xp[0]][xp[1]] == 'true':
        
        #if ((xp[0] == target[0] and xp[1] == target[1])) or t == 10000:
        #        self.goal_reached = True 
        if subgoal_count == 5 or t == 10000:
            self.goal_reached = True



        #rewards,target = reward(xp,self.goal_reached,target)            

        return xp,self.goal_reached
