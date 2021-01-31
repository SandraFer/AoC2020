from itertools import product
import day01

def get_all_neighbors(pos_triple, dims=3):
    m = [-1, 0, 1]
    arrs = [[pos_triple[i]+mi for mi in m] for i in range(dims)]
    if dims == 3:
        neighs = list(product(arrs[0], arrs[1], arrs[2]))
    else:
        neighs = list(product(arrs[0], arrs[1], arrs[2], arrs[3]))
    neighs.pop(neighs.index(pos_triple))
    expt = 3 ** dims - 1
    assert len(neighs) == expt, f'neighbor list is of wrong len {len(neighs)}'
    return neighs

def perform_boot(cycles, active_list, dims=3):
    for _ in range(cycles):
        newly_active = []
        newly_inactive = []
        neighbor_check_list = []
        for entry in active_list:
            my_neighs = get_all_neighbors(entry, dims=dims)
            # count how many are in active list
            act = len([n for n in my_neighs if n in active_list])
            if not 2 <= act <=3:
                newly_inactive.append(entry)
            neighbor_check_list += my_neighs
        neighbor_check_list = list(set(neighbor_check_list))
        neighbor_check_list = [n for n in neighbor_check_list if n not in active_list]

        # use neighbor check list to find inactive fields which can become active
        for entry in neighbor_check_list:
            my_neighs = get_all_neighbors(entry, dims=dims)
            act = len([n for n in my_neighs if n in active_list])
            if act == 3:
                newly_active.append(entry)

        # apply
        for act in newly_inactive:
            idx = active_list.index(act)
            active_list.pop(idx)
        for inact in newly_active:
            active_list.append(inact)
    return active_list

if __name__ == '__main__':
    content = day01.load_data('data17.txt')

    cycles = 6
    dimx = len(content[0])
    dimy = len(content)

    ## part 1
    active_list = []
    z = 0
    for y in range(dimy):
        for x in range(dimx):
            if content[y][x] == '#':
                active_list.append((x,y,z))

    active_list = perform_boot(cycles, active_list)
    print(f'Part 1: {len(active_list)}')

    ## part 2: very slow :(
    active_list = []
    z = 0
    w = 0
    for y in range(dimy):
        for x in range(dimx):
            if content[y][x] == '#':
                active_list.append((x,y,z,w))

    active_list = perform_boot(cycles, active_list, dims=4)
    print(f'Part 2: {len(active_list)}')
