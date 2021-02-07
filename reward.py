from map_details import get_map
import random
from map_details import get_map

map_dat,MAP_WID,MAP_HEI,cell = get_map()

"""def get_rewatd_table():
    map_detail,MAP_WID,MAP_HEI = get_map()
    reward_targets = []
    for i in range(5):
        in_map_p = True
        while in_map_p:
            ini_state = [random.randint(0,MAP_WID-1), random.randint(0,MAP_HEI-1)]
            if map_detail[ini_state[0]][ini_state[1]] == 'false':
                reward_targets.append([ini_state[0],ini_state[1]])
                in_map_p = False
    reward_tab_pos_dic = {}
    for i in range(MAP_WID):
        for j in range(MAP_HEI):
            if map_detail[i][j] == False:
                reward_tab_pos_dic[(i,j)] = 1
            else:
                reward_tab_pos_dic[(i,j)] = -100
    for i in reward_targets:
        reward_tab_pos_dic[(i[0],i[1])] = 1000
    return reward_tab_pos_dic"""

#Reward definition 
"""def reward(state,goal_reached,target):
    r = -1
    remaining_targets=len(target)
    if goal_reached == True:
        r = 1000
    else:
        target_reached = -1
        for i in range(remaining_targets):
            if state[0]==target[i][0] and state[1]==target[i][1]:
                r = 100
                target_reached = i
        if target_reached != -1:
            target.pop(target_reached)
    return r,target"""

"""def reward(target,new_state,subgoal,subgoal_count,gamma,prev_subgoal_count,visited,number_of_subgoals):
    #r = -1
    if new_state not in visited and ((new_state[0]==subgoal[0][0] and new_state[1]==subgoal[0][1]) or (new_state[0]==subgoal[1][0] and new_state[1]==subgoal[1][1]) or (new_state[0]==subgoal[2][0] and new_state[1]==subgoal[2][1]) or (new_state[0]==subgoal[3][0] and new_state[1]==subgoal[3][1])):
        subgoal_count+=1 
        visited.append(new_state)
    #r = -1 - gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*80) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*80)
    if subgoal_count==4 and (new_state[0]==target[0] and new_state[1]==target[1]):
        subgoal_count+=1 
        visited.append(new_state)
    # Working reward for 2 subgoals
    #r = -(abs(new_state[0]-target[0])+abs(new_state[1]-target[1])) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*56) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*56)
    #r = - gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*0.7) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*0.7)
    if subgoal_count==0:
        r = -(abs(new_state[0]-subgoal[0][0])+abs(new_state[1]-subgoal[0][1])) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*65) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*65)
    elif subgoal_count==1:
        r = -(abs(new_state[0]-subgoal[1][0])+abs(new_state[1]-subgoal[1][1])) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*65) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*65)
    elif subgoal_count==2:
        r = -(abs(new_state[0]-subgoal[2][0])+abs(new_state[1]-subgoal[2][1])) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*65) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*65)
    elif subgoal_count==3:
        r = -(abs(new_state[0]-subgoal[3][0])+abs(new_state[1]-subgoal[3][1])) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*65) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*65)
    elif subgoal_count==4:
        r = -(abs(new_state[0]-target[0])+abs(new_state[1]-target[1])/6.5) -  gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*65) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*65)"""
    #return r,subgoal_count,visited
    
def reward(new_state,subgoal,subgoal_count,gamma,prev_subgoal_count,visited,number_of_subgoals):
    #r = -1
    if new_state not in visited and ((new_state[0]==subgoal[0][0] and new_state[1]==subgoal[0][1]) or (new_state[0]==subgoal[1][0] and new_state[1]==subgoal[1][1]) or (new_state[0]==subgoal[2][0] and new_state[1]==subgoal[2][1]) or (new_state[0]==subgoal[3][0] and new_state[1]==subgoal[3][1]) or (new_state[0]==subgoal[4][0] and new_state[1]==subgoal[4][1])):
        subgoal_count+=1 
        visited.append(new_state)
        #r=200
        #r = -1 + gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*0.7) + (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*0.7)
    r = -1 - gamma * (((number_of_subgoals-subgoal_count-0.5)/number_of_subgoals)*56) - (((number_of_subgoals-prev_subgoal_count-0.5)/number_of_subgoals)*56)
    if map_dat[new_state[0]][new_state[1]]=="true":
        r =-10000
    return r,subgoal_count,visited 


    """if goal_reached == True:
        return 100 * subgoal_count ,subgoal_count
    else:
        r = -((abs(new_state[0]-target[0])+abs(new_state[1]-target[1])))
        if subgoal_count == 0:
            #r = -((abs(new_state[0]-subgoal[0][0])+abs(new_state[1]-subgoal[0][1])))
            if (new_state[0]==subgoal[0][0] and new_state[1]==subgoal[0][1]):
                #print("Reached 1")
                r = 25
                subgoal_count += 1
        elif subgoal_count == 1:
            #r = -((abs(new_state[0]-subgoal[1][0])+abs(new_state[1]-subgoal[1][1])))
            if (new_state[0]==subgoal[1][0] and new_state[1]==subgoal[1][1]):
                #print("Reached 2")
                r = 25
                subgoal_count += 1 
        elif subgoal_count == 1 or subgoal_count == 2:
            #r = -((abs(new_state[0]-target[0])+abs(new_state[1]-target[1])))
            if ((new_state[0]==subgoal[0][0] and new_state[1]==subgoal[0][1]) or (new_state[0]==subgoal[1][0] and new_state[1]==subgoal[1][1])):
                #print("Reached 3")
                r = -25
        return r,subgoal_count"""

