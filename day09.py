import day01

def find_sum_pair(a_target, a_list):
    """ find whether there are two numbers in a_list whose sum is a_target """
    j = 0
    found_pair = False
    while j < len(a_list)-1 and not found_pair:
        if a_target - a_list[j] in a_list[j+1:]:
            found_pair = True
        j += 1
    return found_pair

if __name__ == '__main__':
    content = day01.load_data('data09.txt')
    content = list(map(int, content))

    ## part 1
    preamble = 25
    i = preamble
    all_good = True
    target2 = None

    while i < len(content) and all_good:
        ok = find_sum_pair(content[i], content[i-preamble:i])
        if not ok:
            all_good = False
            print(f'Part 1: First number to break rules is {content[i]}')
            target2 = content[i]
        i += 1

    # part 2
    top_ind = content.index(target2)
    found = False

    j_end = top_ind
    j_start = j_end - 2
    my_sum = sum(content[j_start:j_end])
    while not found:
        if my_sum > target2:
            j_end -= 1
            j_start= j_end - 2
            my_sum = sum(content[j_start:j_end])
        elif my_sum < target2:
            j_start -= 1
            my_sum += content[j_start]
        else:
            found = True
    # print(f'Elements {j_start} up to {j_end-1} give us the right sum')
    assert sum(content[j_start:j_end]) == target2

    print(f'Part 2: Encryption weakness is {min(content[j_start:j_end]) + max(content[j_start:j_end])}')
    