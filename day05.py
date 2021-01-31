import day01

def char2bin(a_char):
    if a_char in ['B', 'R']:
        return '1'
    elif a_char in ['F', 'L']:
        return '0'
    else:
        raise NotImplementedError(f'Unknown character {a_char}')

def str2val(a_str):
    """ Turn seat name into number """
    assert len(a_str) == 10, f'malformed string'
    row = int(''.join(map(char2bin, a_str[:7])), 2)
    col = int(''.join(map(char2bin, a_str[7:])), 2)
    return row * 8 + col

if __name__ == '__main__':
    content = day01.load_data('data05.txt')

    seat_ids = list(map(str2val, content))

    ## part 1
    print(f'Highest seat number is: {max(seat_ids)} (part 1)')

    ## part 2
    not_in_list_but_neighbors = [i-1 for i in seat_ids if i-1 not in seat_ids and i-2 in seat_ids]
    print(f'My seat number is: {not_in_list_but_neighbors[0]} (part 2)')
