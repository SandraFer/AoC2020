import re
import day01

def decipher(a_str):
    dir_list = []
    while len(a_str) > 0:
        if re.match(r'[ew]', a_str):
            dir_list.append(a_str[0])
            a_str = a_str[1:]
        else:
            dir_list.append(a_str[:2])
            a_str = a_str[2:]
    return dir_list

def move_in_hex_grid(pos, dir_list):
    # x-axis: w-e axis
    # y-axis: sw-ne axis
    dirs = {'ne': (0, 1), 'e': (1, 0), 'se': (1, -1), 
            'nw':(-1, 1), 'w': (-1, 0), 'sw': (0, -1)}
    for d in dir_list:
        pos[0] += dirs[d][0]
        pos[1] += dirs[d][1]
    return pos

def daily_flip(tile_dict, adjacent_dict):
    black_tiles = [k for k, v in tile_dict.items() if v]
    neighbors = ['ne', 'e', 'se', 'nw', 'w', 'sw']

    neighs = []

    for bt in black_tiles:
        if bt in adjacent_dict.keys():
            my_neighbors = adjacent_dict[bt]
        else:
            bt_int = [int(x) for x in bt.split(',')]
            my_neighbors = [move_in_hex_grid(bt_int[:], [n]) for n in neighbors]
            adjacent_dict[bt] = my_neighbors[:]
        bl = 0
        for p in my_neighbors:
            if f'{p[0]},{p[1]}' in black_tiles:
                bl += 1
            elif f'{p[0]},{p[1]}' not in neighs:
                neighs.append(f'{p[0]},{p[1]}')
        if bl == 0 or bl > 2:
            tile_dict[bt] = False

    for wt in neighs:
        if wt in adjacent_dict:
            my_neighbors = adjacent_dict[wt]
        else:
            wt_int = [int(x) for x in wt.split(',')]
            my_neighbors = [move_in_hex_grid(wt_int[:], [n]) for n in neighbors]
            adjacent_dict[wt] = my_neighbors[:]
        bl = 0
        for p in my_neighbors:
            if f'{p[0]},{p[1]}' in black_tiles:
                bl += 1
        if bl == 2:
            tile_dict[wt] = True

if __name__ == "__main__":
    content = day01.load_data('data24.txt')

    ## part 1
    tile_dict = {}
    for c in content:
        li = decipher(c)
        p = move_in_hex_grid([0, 0], li)
        # use string representation of index as dictionary key
        p_key = f'{p[0]},{p[1]}'
        if p_key in tile_dict.keys():
            tile_dict[p_key] = not tile_dict[p_key]
        else:
            tile_dict[p_key] = True
    # black tile = True
    print(f'Part 1: {list(tile_dict.values()).count(True)}')

    ## part 2
    adjacent_dict = {}
    for _ in range(100):
        daily_flip(tile_dict, adjacent_dict)
    print(f'Part 2: {list(tile_dict.values()).count(True)}')
