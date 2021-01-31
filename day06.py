import day01

def single_answers(a_str):
    return set(a_str.replace(';', ''))

def number_of_answers_per_group(a_str):
    return len(single_answers(a_str))

def number_of_unanimous_yes(a_str):
    entries = a_str.split(';')
    answers = single_answers(a_str)
    in_all = []
    for a in answers:
        gotit = [a in e for e in entries]
        if False not in gotit:
            in_all.append(a)
    return len(in_all)

if __name__ == '__main__':
    content = day01.load_data('data06.txt')

    # split input into groups
    groups = []
    cur_group = ''
    for c in content:
        if len(c) == 0:
            groups.append(cur_group)
            cur_group = ''
        else:
            if len(cur_group) == 0:
                cur_group = c
            else:
                cur_group += f';{c}'
    if len(cur_group) > 0:
        groups.append(cur_group)

    ## part 1
    num_asw = list(map(number_of_answers_per_group, groups))
    print(f'Part 1: {sum(num_asw)}')

    ## part 2
    num_asw = list(map(number_of_unanimous_yes, groups))
    print(f'Part 2: {sum(num_asw)}')
