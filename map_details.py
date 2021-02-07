import json


MAP_WID=50
MAP_HEI=50


def get_map():
    with open('data15.json') as f:
        data = json.load(f)
    keys_to_extract = ["map"]
    map_d = {key: data[key] for key in keys_to_extract}
    res1 ={}
    for key,values in map_d.items():
        res1 = values

    map_data = [[0 for i in range(MAP_WID)] for j in range(MAP_HEI)]
    keys_to_extract1 = ['x', 'y','isWall']

    for i in range(len(res1)):
        res = res1[i]
        x = res.get('x')
        y = res.get('y')
        wal = res.get('isWall')
        map_data[x][y] = wal

    cell_count = 0
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j]=="true":
                cell_count += 1

    return map_data,MAP_WID,MAP_HEI,cell_count
