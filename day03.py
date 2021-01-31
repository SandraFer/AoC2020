from itertools import product
import day01

def check_encounters(a_slope, a_content):
    map_width = len(a_content[0])

    tree = '#'
    cur_x = 0
    cur_y = 0
    tree_count = 0 if content[cur_y][cur_x] != tree else 1

    while cur_y < len(a_content)-a_slope[1]:
        cur_x = (cur_x + a_slope[0]) % map_width
        cur_y += a_slope[1]
        next_field = content[cur_y][cur_x]
        tree_count += int(next_field == tree)
    return tree_count

if __name__ == '__main__':
    content = day01.load_data('data03.txt')

    ## part 1
    tree_count = check_encounters((3, 1), content)
    print(f'Part 1: Encountered {tree_count} trees')

    ## part 2
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    tot = 1

    for slope in slopes:
        tree_count = check_encounters(slope, content)
        # print(f'slope: {slope} -> {tree_count} encounters')
        tot *= tree_count
    print(f'Part 2: Multiplication of all tree encounters: {tot}')
