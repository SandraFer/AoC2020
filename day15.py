def solve(a_content, a_target):
    numbers = list(map(int, a_content.split(',')))
    num_dict = dict((x, [j]) for j, x in enumerate(numbers[:-1]))
    cnt = len(numbers)-1

    while cnt < a_target-1:
        act = numbers[-1]

        if act not in num_dict.keys():
            next_num = 0
            num_dict[act] = []
        else:
            next_num = cnt - num_dict[act][-1]
        num_dict[act].append(cnt)
        
        numbers.append(next_num)
        cnt += 1

    assert len(numbers) == a_target, f'{len(numbers)}'
    return numbers[-1]

if __name__ == '__main__':
    content = '0,14,6,20,1,4'

    ## part 1
    print(f'Part 1: {solve(content, 2020)}')

    ## part 2
    print(f'Part 2: {solve(content, 30000000)}')
