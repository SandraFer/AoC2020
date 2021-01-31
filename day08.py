import day01

def decipher_cmd(a_cmd):
    (c, v) = a_cmd.split(' ')
    assert c in ['nop', 'jmp', 'acc'], f'unknown command {c}'
    return c, int(v)

def run_booter(a_content):
    acc = 0
    executed = []
    cur_line = 0
    all_good = True

    while all_good and cur_line < len(a_content):
        (cmd, val) = decipher_cmd(a_content[cur_line])
        if cmd == 'nop':
            next_line = cur_line + 1
        elif cmd == 'acc':
            next_line = cur_line + 1
            acc += val
        else:
            next_line = cur_line + val
        if next_line in executed:
            #print(f'forward: found infinite loop on line {cur_line}!')
            all_good = False
            executed.append(cur_line)
            executed.append(next_line)
        else:
            executed.append(cur_line)
            cur_line = next_line
    return acc, executed, all_good

if __name__ == '__main__':
    content = day01.load_data('data08.txt')
    
    ## part 1
    accumulator, executed_lines, thr = run_booter(content)
    if not thr:
        print(f'Part 1: Accumulator value before infinite loop: {accumulator}')
        
    ## part 2
    # find loop
    looper = executed_lines[-1]
    in_loop = executed_lines[executed_lines.index(looper)+1:-1]

    # keep nop and jmp only
    keepers = []
    for j in in_loop:
        (cmd, _) = decipher_cmd(content[j])
        if cmd in ['nop', 'jmp']:
            keepers.append(j)
    
    # brute force it
    for k in keepers:
        (cmd, _) = decipher_cmd(content[k])
        old_line = content[k]
        if cmd == 'nop':
            new_line = old_line.replace('nop', 'jmp')
        else:
            new_line = old_line.replace('jmp', 'nop')
        content[k] = new_line
        acc, _, thr = run_booter(content)
        if thr:
            print(f'ran through by changing line {k} to {new_line}! accumulator value: {acc}')
            break
        else:
            content[k] = old_line
