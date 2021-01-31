import re
import day01

def solve_new_math(a_str):
    val = 0
    a_str = a_str.replace(' ', '')
    if '(' not in a_str:
        vals = list(map(int, re.split(r'\+|\*', a_str)))
        sgns = re.findall(r'\+|\*', a_str)
        val = vals[0]
        for i in range(len(sgns)):
            if sgns[i] == '+':
                val += vals[i+1]
            elif sgns[i] == '*':
                val *= vals[i+1]
    else:
        substr = re.findall(r'\([^()]*\)', a_str)
        for s in substr:
            v = solve_new_math(s[1:-1])
            a_str = a_str.replace(s, f'{v}')
        val = solve_new_math(a_str)
    return val

def solve_new_math_advanced(a_str):
    val = 0
    a_str = a_str.replace(' ', '')
    if '(' not in a_str:
        if '+' in a_str:
            while '+' in a_str:
                vals = re.search(r'\d+\+\d+', a_str)
                v = vals.group(0)
                ins = int(v.split('+')[0]) + int(v.split('+')[1])
                a_str = a_str[:vals.span()[0]] + f'{ins}' + a_str[vals.span()[1]:]
        vals = list(map(int, re.split(r'\*', a_str)))
        sgns = re.findall(r'\*', a_str)
        val = vals[0]
        for i in range(len(sgns)):
            val *= vals[i+1]
    else:
        substr = re.findall(r'\([^()]*\)', a_str)
        for s in substr:
            v = solve_new_math_advanced(s[1:-1])
            a_str = a_str.replace(s, f'{v}')
        val = solve_new_math_advanced(a_str)
    return val

if __name__ == '__main__':
    content = day01.load_data('data18.txt')

    ## part 1
    tot = 0
    for c in content:
        tot += solve_new_math(c)
    print(f'Part 1: {tot}')

    ## part 2
    tot = 0
    for c in content:
        tot += solve_new_math_advanced(c)
    print(f'Part 2: {tot}')
