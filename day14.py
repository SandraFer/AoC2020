import day01

def apply_mask_to_val(a_val, a_mask):
    new_val = ''
    for v, m in zip(a_val, a_mask):
        if m == 'X':
            new_val += v
        else:
            new_val += m
    return new_val

def apply_mask_to_add(a_val, a_mask):
    new_val = ''
    for v, m in zip(a_val, a_mask):
        if m == '0':
            new_val += v
        else:
            new_val += m
    # count floating bits
    floats = new_val.count('X')
    f = f'{{:0{floats}b}}'
    idxs = [j for j, x in enumerate(new_val) if x == 'X']
    vals = []
    for i in range(2**floats):
        inserts = f.format(i)
        my_val = new_val
        for j in range(floats):
            my_val = my_val[:idxs[j]] + inserts[j] + my_val[idxs[j]+1:]
        vals.append(my_val)

    return vals

if __name__ == '__main__':
    content = day01.load_data('data14.txt')

    bits = 36
    frmt = f'{{:0{bits}b}}'

    ## part 1
    mem = {}
    mask = ''
    for c in content:
        (s1, s2) = c.split(' = ')
        if s1 == 'mask':
            mask = s2
        else:
            slt = int(s1.split('[')[1].split(']')[0])
            val = apply_mask_to_val(frmt.format(int(s2)), mask)
            mem[slt] = int(val, 2)
    print(sum(mem.values()))

    ## part 2
    mem = {}
    mask = ''
    for c in content:
        (s1, s2) = c.split(' = ')
        if s1 == 'mask':
            mask = s2
        else:
            slt = int(s1.split('[')[1].split(']')[0])
            slts = apply_mask_to_add(frmt.format(int(slt)), mask)
            for slt in slts:
                mem[slt] = int(s2)
    print(sum(mem.values()))
