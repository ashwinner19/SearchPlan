# modules
import gzip
import math
import numpy as np

import tcod as libtcod
import pygame

# game file
import constants
import pickle
from matplotlib import pyplot
from neighborhood_functions import avg_components
from moving_window_filter import moving_window_filter
from calculate_profile import profile
from calculate_profile import entropy
import json
import sys


sys.setrecursionlimit(100000)

# STRUCTURE DEFINITION
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path


# OBJECTS
class obj_Room:

    def __init__(self, coords, size):
        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    def intersect(self, other):
        # return true if other object intersects
        objects_intersects = (self.x1 <= other.x2 and self.x2 >= other.x1 and
                              self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersects


# MAP DEFINITION
def map_create():
    global number_of_rooms, room_key, room_dict, tunnel_key, tunnel_dict
    new_map = [[struc_Tile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    # generate new room
    list_of_rooms = []
    room_key = 1
    tunnel_key = 11
    room_dict = {}
    tunnel_dict = {}

    for i in range(constants.MAP_MAX_NUM_ROOMS):

        w = libtcod.random_get_int(0, constants.ROOM_MIN_WIDTH,
                                   constants.ROOM_MAX_WIDTH)
        h = libtcod.random_get_int(0, constants.ROOM_MIN_HEIGHT,
                                   constants.ROOM_MAX_HEIGHT)
        x = libtcod.random_get_int(0, 2, constants.MAP_WIDTH - w - 2)
        y = libtcod.random_get_int(0, 2, constants.MAP_HEIGHT - h - 2)

        # create room
        new_room = obj_Room((x, y), (w, h))
        failed = False

        # check for interference
        for other_room in list_of_rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        # place the room
        if not failed:
            map_create_room(new_map, new_room)
            room_key = room_key + 1
            current_center = new_room.center
            if len(list_of_rooms) == 0:
                print("length of list_of_rooms is zero")
            else:
                previous_center = list_of_rooms[-1].center
                # dig the tunnels
                map_create_tunnels(current_center, previous_center, new_map)
                tunnel_key = tunnel_key + 1

            list_of_rooms.append(new_room)
    number_of_rooms = len(list_of_rooms)
    print ("Room", room_dict)
    print("Tunnel:", tunnel_dict)

    return new_map


def map_create_room(new_map, new_room):
    global total_num_room_cells, room_key, room_dict
    room_coords = []
    list = []
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            new_map[x][y].block_path = False
            total_num_room_cells = total_num_room_cells + 1
            room_coords.append([x, y])
    #print("Unsorted",room_coords)
    #list = sorted(room_coords,key= lambda x:x[0])
    #print("Sorted",list)
    room_dict[room_key] = room_coords


def map_create_tunnels(coords1, coords2, new_map):
    global total_num_tunnel_cells, tunnel_key, tunnel_dict
    x1, y1 = coords1
    x2, y2 = coords2
    tunnel_coords = []

    coin_flip = (libtcod.random_get_int(0, 0, 1) == 1)
    print ("1st:",x1,y1)
    tunnel_coords.append([x1, y1])
    if coin_flip:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if new_map[x][y1].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            if new_map[x][y1+1].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            new_map[x][y1].block_path = False
            new_map[x][y1+1].block_path = False
            tunnel_coords.append([x, y1])
            tunnel_coords.append([x, y1+1])
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if new_map[x2][y].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            if new_map[x2+1][y].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            new_map[x2][y].block_path = False
            new_map[x2+1][y].block_path = False
            tunnel_coords.append([x2, y])
            tunnel_coords.append([x2+1, y])

    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if new_map[x1][y].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            if new_map[x1+1][y].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            new_map[x1][y].block_path = False
            new_map[x1+1][y].block_path = False
            tunnel_coords.append([x1, y])
            tunnel_coords.append([x1+1, y])

        for x in range(min(x1, x2), max(x1, x2) + 1):
            if new_map[x][y2].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            if new_map[x][y2+1].block_path == True:
                total_num_tunnel_cells = total_num_tunnel_cells + 1
            new_map[x][y2].block_path = False
            new_map[x][y2+1].block_path = False
            tunnel_coords.append([x, y2])
            tunnel_coords.append([x, y2+1])
    tunnel_coords.append([x2, y2])
    tunnel_dict[tunnel_key] = tunnel_coords

# DRAWING DEFINITION
def draw_game():
    global SURFACE_MAIN

    # clear surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # update display
    pygame.display.flip()

def draw_map(map_to_draw):
    global map_detail
    map_detail = map_to_draw
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                SURFACE_MAIN.blit(constants.WALL, (x * constants.CELL_WIDTH, y * constants.CEL_HEIGHT))

            else:
                SURFACE_MAIN.blit(constants.FLOOR, (x * constants.CELL_WIDTH, y * constants.CEL_HEIGHT))


# GAME DEFINITION
def game_main_loop():
    '''Main game is looped to be active'''
    game_quit = False

    while not game_quit:
        events_list = pygame.event.get()

        for event in events_list:
            if event.type == pygame.QUIT:
                # Calculate Shannon Entropy
                calculate_entropy()
                quit_game()

        # draw game
        draw_game()


def game_initialize():
    '''initialize game and pygame'''
    global SURFACE_MAIN, GAME_MAP
    global PLAYER

    #COMPLEXITY INITIAL
    com_initial()

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CEL_HEIGHT))

    GAME_MAP = map_create()


def quit_game():
    '''saving game'''
    #save_game()
    '''Now exit'''
    pygame.quit()
    exit()


# SAVING THE GAME
def save_game():
    global GAME_MAP
    number = str(constants.SAVE)

    with gzip.open('savedata/savegame'+number, 'wb') as file:
        pickle.dump([GAME_MAP], file)


# COMPLEXITY
def com_initial():
    global total_num_room_cells, total_num_tunnel_cells

    total_num_room_cells = 0
    total_num_tunnel_cells = 0

"""def calculate_entropy():
    global total_num_room_cells, total_num_tunnel_cells, number_of_rooms
    '''
    SHANNON Entropy of list of numbers is given by:
    H(x) = - Σ  P(xi) log2 P(xi) 
    '''
    total_cells_uncarved = total_num_room_cells + total_num_tunnel_cells

    total_size_of_map = constants.MAP_WIDTH * constants.MAP_HEIGHT

    # probability of cells of room
    P1 = cal_prob(total_num_room_cells, total_cells_uncarved)

    # probability of cells of tunnels
    if total_num_tunnel_cells != 0:
        P2 = cal_prob(total_num_tunnel_cells, total_cells_uncarved)
    # probability of number of rooms
    P3 = cal_prob(number_of_rooms, constants.MAP_MAX_NUM_ROOMS)

    # probability of whole map built
    P4 = cal_prob(total_cells_uncarved, total_size_of_map)

    # SHANNON ENTROPY
    H1 = - (P1 * math.log2(P1))
    if total_num_tunnel_cells != 0:
        H2 = - (P2 * math.log2(P2))
    else:
        H2 = 0
    H3 = - (P3 * math.log2(P3))
    H4 = - (P4 * math.log2(P4))

    H = (H1 + H2 + H3 + H4) / 4
    print("Entropy of map:", H)


# CALCULATING PROBABILITY
def cal_prob(a, b):
    Probability = a / b

    return Probability"""

"""def calculate_entropy():
    final_matrix1 = []
    final_matrix = []
    for x in range(0, constants.MAP_WIDTH):
        matrices = []
        for y in range(0, constants.MAP_HEIGHT):
            if map_detail[x][y].block_path == False:
                matrices.append(1)
            else:
                matrices.append(0)
        final_matrix.append(matrices)
    final_matrix1 = np.array([final_matrix])

    F = avg_components
    for m in range(0, len(final_matrix1)):
        active_matrix = final_matrix1[m]
        print("---------\nMatrix #{0}\n---------\n".format(m))

        # Produce the filtered matrices at varying scales and the associated
        # entropy "profiles"
        matrices1 = []
        for n in range(1, min(active_matrix.shape)):
            output_matrix = moving_window_filter(matrix=active_matrix,
                                                 f=F,
                                                 neighborhood_size=n)
            matrices1.append(output_matrix)
            print("Neighborhood size = {0}\n{1}\n".format(n, output_matrix))

        print("Profile:\n{0}\n".format(profile(matrices1)))
        a = profile(matrices1)
        print("Network Entropy", max(a))"""


def calculate_network_entropy(a):
    global temp, number_of_rooms, k_temp,H_final
    k = []
    P = []
    S = []
    H = []
    k_temp = 0
    temp = 0

    N = len(a)
    print (N)
    print (a)
    M = float(N-1)


    #Calculating node degree k[i]
    for i in range(0, N):
        k_temp = 0
        for j in range(0, N):
            k_temp += a[i][j]
        k.append(k_temp)
    print

    #Calculating Probability distribution
    for i in range(0, N):
        b = []
        for j in range(0, N):
            b.append(0)
        P.append(b)
    for i in range(0, N):
        for j in range(0, N):
            if a[i][j] == 0:
                P[i][j] = 0
            else:
                P[i][j] = 1/k[i]

    #Calculating entropy forr each node
    """S_temp = 0
    for i in range(0, N):
         S_temp = math.log2(k[i])
         S.append(S_temp)"""


    #Calculating normalized node entropy
    H_temp = 0
    for i in range(0, N):
        if N-1 == 1 :
            H_temp = 1
        else:
            H_temp = (math.log2(k[i]))/(math.log2(N-1))
        H.append(H_temp)
    print(H)

    #Normalized Network Entropy
    for i in range(0, N):
        temp += H[i]

    H_final = (1.0/N) * temp

    print ("Network Entropy:", H_final)
    
    write_to_json()




#def matrix_generation():
def calculate_entropy():
    # Rooms= 1, wall= 0, tunnel= 2
    global room_dict, tunnel_dict, final_mat,  number_of_rooms,rooms_dict, room_done, path
    final_mat = []
    matrix =[]
    a = []
    room_coords = []
    rooms_dict = {}
    room_key = 1
    final = []

    for x in range(0, number_of_rooms):
        b = []
        for y in range(0, number_of_rooms):
            b.append(0)
        a.append(b)

    for x in range(0,constants.MAP_WIDTH):
        matrix1 = []
        for y in range(0, constants.MAP_HEIGHT):
            matrix1.append(0)
        matrix.append(matrix1)

    for k, v in room_dict.items():
        room_coords = []
        for x, y in v:
            matrix[x][y] = 1
            room_coords.append((x, y))
        rooms_dict[room_key] = room_coords
        room_key += 1
    print ("ASH",rooms_dict)

    for k1, v1 in tunnel_dict.items():
        for x1, y1 in v1:
            if matrix[x1][y1] == 0:
                matrix[x1][y1] = 2

    print (matrix)
    num_rom = len(rooms_dict.keys())
    print (num_rom)

    for r in range(1, num_rom+1):

        for k, v in room_dict.items():
            room_coords = []
            for x, y in v:
                matrix[x][y] = 1
                room_coords.append((x, y))
            rooms_dict[room_key] = room_coords
            room_key += 1
        print ("ASH", rooms_dict)

        for k1, v1 in tunnel_dict.items():
            for x1, y1 in v1:
                if matrix[x1][y1] == 0 or matrix[x1][y1] == 3:
                    matrix[x1][y1] = 2

        room_done =[]
        room_values = rooms_dict.get(r)
        path =[]
        print (room_values,"\n")
        i, j = room_values[1]
        print(i,j)
        print ("Che", matrix)
        a = traverse(i, j, r, matrix, room_values, a)
        print (a)
    calculate_network_entropy(a)


def traverse(i,j,r,matrix,room_values,a):
    global room_done, path
    room = int(r)

    done = room_values[1]
    if i >= len(matrix) or j >= len(matrix[0]) or i < 0 or j < 0 or matrix[i][j] == 0 or matrix[i][j] == 3:
        print ("Ash1", (i, j))
        return a
    elif matrix[i][j] == 1:
        if (i, j) in room_values:
            print ("Ash2", (i, j))
            tmp = matrix[i][j]
            matrix[i][j] = 3
            traverse(i, j + 1, r, matrix, room_values, a)
            traverse(i, j - 1, r, matrix, room_values, a)
            traverse(i + 1, j, r, matrix, room_values, a)
            traverse(i - 1, j, r, matrix, room_values, a)
            path.append((i, j))
            return a
        else:
            b = get_key((i, j))
            print ("ASH3", room, b)
            if b not in room_done:
                a[room - 1][b - 1] = 1
                room_done.append(room)
            return a
    elif matrix[i][j] == 2:
        print ("Ash4", (i, j))
        tmp = matrix[i][j]
        matrix[i][j] = 3
        traverse(i, j + 1, r, matrix, room_values, a)
        traverse(i, j - 1, r, matrix, room_values, a)
        traverse(i + 1, j, r, matrix, room_values, a)
        traverse(i - 1, j, r, matrix, room_values, a)
        return a


def get_key(val):
    global rooms_dict
    print("A", val)
    for key, value in rooms_dict.items():
        for v in value:
            if val == v:
                return int(key)


def write_to_json():
    global GAME_MAP, H_final, number_of_rooms
    print("number_of_rooms",number_of_rooms)
    map_detail = GAME_MAP
    data = {}
    data['map'] = []
    data['dimensions'] = []
    data['network entropy'] =[]
    data['dimensions'].append({'rows': constants.MAP_HEIGHT,
    	                       'colums': constants.MAP_WIDTH})
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_detail[x][y].block_path == True:
                data['map'].append({'x' : x,
                              'y' : y,
                              'isWall' : 'true',
                              'isOccupied' : 'false',
                              'isExplored' : 'false'
                              })

            else:
                data['map'].append({'x' : x,
                              'y' : y,
                              'isWall' : 'false',
                              'isOccupied' : 'false',
                              'isExplored' : 'false'
                              })
    data['network entropy'].append({'complexity':H_final})
    with open('data16.json', 'w') as outfile:
        json.dump(data, outfile)


# EXECUTION
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
