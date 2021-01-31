import day01

if __name__ == '__main__':
    content = day01.load_data('data10.txt')

    ## part 1
    diffdict = {1: 0, 2: 0, 3: 0}

    adapters = sorted(map(int, content))
    last_value = 0
    difflist = []
    for a in adapters:
        if a-last_value in diffdict.keys():
            difflist.append(a-last_value)
            diffdict[a-last_value] += 1
            last_value = a
        else:
            print(f'Illegal difference: {a-last_value}')
    assert sum(diffdict.values()) == len(content)

    diffdict[3] += 1  # add device adapter!!!
    difflist.append(3)
    print(f'Part 1: 1-diff times 3-diff: {diffdict[1] * diffdict[3]}')

    # part 2
    all_threes = []
    for j, a in enumerate(difflist):
        if a == 3:
            all_threes.append(j)

    groups_of_1 = [all_threes[0]]+[all_threes[j+1]-all_threes[j]-1 for j in range(len(all_threes)-1)]
    groups_of_1 = [x-1 for x in groups_of_1 if x > 1]

    total = 1
    for g in groups_of_1:
        if g < 3:
            total *= 2**g
        else:
            total *= (2**g-1)
    print(f'Part 2: {total} different ways to arrange adapters')
