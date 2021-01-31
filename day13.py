import day01

if __name__ == '__main__':
    content = day01.load_data('data13.txt')

    tstamp = int(content[0])
    bus_lines = content[1].split(',')
    serviced_ids = [int(x) for x in bus_lines if x != 'x']

    ## part 1
    min_wait_per_id = [(tstamp//si+1)*si-tstamp for si in serviced_ids]
    my_wait = min(min_wait_per_id)
    my_line = serviced_ids[min_wait_per_id.index(my_wait)]
    print(my_wait*my_line)

    ## part 2: REALLY UGLY
    spacing = serviced_ids[0]
    tstamp = spacing
    others = sorted(serviced_ids[1:])[::-1]
    offset = [bus_lines.index(str(x)) for x in others]

    b = [o%spacing for si, o in zip(others, offset)]
    a = [o%spacing%si for si, o in zip(others, offset)]

    # tstamp spacing
    b_off = []
    a_plus_1 = 1
    for j, ai in enumerate(a):
        if ai == 0:
            a_plus_1 *= others[j]
            b_off.append(0)
        else:
            if offset[j] > spacing:
                b_off.append(offset[j]-spacing)  # we want a+1 as factor
            else:
                b_off.append(offset[j]+others[j]-spacing)  # we want a+1 as factor

    cand_a = a_plus_1  # tstamp = spacing * (a_plus_1-1)

    other_a = [others[j] for j in range(len(others)) if b_off[j] != 0]
    offset_a = [offset[j] for j in range(len(others)) if b_off[j] != 0]
    b_off = [b_off[j] for j in range(len(others)) if b_off[j] != 0]

    # brute force
    got_it = False
    while not got_it:
        cand_a += a_plus_1
        tstamp = spacing*(cand_a-1)
        check = [(tstamp+to)%si==0 for (si, to) in zip(other_a, offset_a)]
        if False not in check:
            got_it = True

    tstamp = spacing*(cand_a-1)
    print(tstamp)
