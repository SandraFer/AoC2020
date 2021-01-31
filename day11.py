from itertools import product
import day01

def occupy(o, s, cont):
    def occ_filter(item):
        neigh = [cont[x] for x in item[1]]
        if neigh.count(o) == 0 and cont[item[0]] == s:
            return True
        else: 
            return False
    return occ_filter

def empty(o, s, cont, a_tol):
    def emp_filter(item):
        neigh = [cont[x] for x in item[1]]
        if neigh.count(o) >= a_tol and cont[item[0]] == o:
            return True
        else: 
            return False
    return emp_filter

def change_seats(c_str, idx_change, target):
    for idx in idx_change:
        c_str = c_str[:idx] + target + c_str[idx+1:]
    return c_str

def run_complete_seating(a_occ_tol, a_content, a_adjacent_dict, seat, occ):
    content_str = ''
    for c in a_content:
        content_str += c
    cnt = 0
    still_changing = True

    while still_changing:
        if cnt % 2 == 0:
            tg = occ
            fil = occupy(occ, seat, content_str)
        else:
            tg = seat
            fil = empty(occ, seat, content_str, a_occ_tol)

        change_full = filter(fil, a_adjacent_dict.items())
        change = [x[0] for x in change_full]
        if len(change) == 0:
            still_changing = False
        else:
            content_str = change_seats(content_str, change, tg)
        cnt += 1
    print(f'{content_str.count(occ)} seats are occupied')

if __name__ == '__main__':
    content = day01.load_data('data11.txt')

    seat = 'L'
    occ = '#'
    floor = '.'
    width = len(content[0])
    height = len(content)

    ## part 1
    adjacent_dict = {}
    for y in range(height):
        y_bt = max(0, y-1)
        y_tp = min(height-1, y+1)
        for x in range(width):
            x_tp = min(width-1, x+1)
            x_bt = max(0, x-1)
            me = y*width+x
            my_neigh = [dy*width+dx for (dy, dx) in product(range(y_bt, y_tp+1), range(x_bt, x_tp+1))]
            my_neigh.pop(my_neigh.index(me))
            assert len(my_neigh) in [3, 5, 8]
            adjacent_dict[me] = sorted(my_neigh)
    run_complete_seating(4, content, adjacent_dict, seat, occ)

    ## part 2
    # new adjacent dict
    adjacent_dict = {}
    y_bt = 0
    y_tp = height-1
    x_tp = width-1
    x_bt = 0
    dirs = list(product(range(-1, 2), range(-1, 2)))
    dirs.pop(dirs.index((0, 0)))
    for y in range(height):
        for x in range(width):
            me = y*width+x
            my_neigh = []
            for d in dirs:
                nxt_x = x + d[0]
                nxt_y = y + d[1]
                got_it = False
                while y_bt <= nxt_y <= y_tp and x_bt <= nxt_x <= x_tp and not got_it:
                    if content[nxt_y][nxt_x] != floor:
                        got_it = True
                        my_neigh.append(nxt_y*width+nxt_x)
                    else:
                        nxt_x += d[0]
                        nxt_y += d[1]
            if me in my_neigh:
                my_neigh.pop(my_neigh.index(me))
            adjacent_dict[me] = sorted(set(my_neigh))
    run_complete_seating(5, content, adjacent_dict, seat, occ)
