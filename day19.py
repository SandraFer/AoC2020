import re
import day01

def find_regex_part1(target_dict, raw_rules):
    transformed = list(target_dict.keys())
    untransformed = list([x for x in raw_rules.keys() if x not in target_dict.keys()])
    new_rules = dict((k, v) for k, v in raw_rules.items())

    while len(untransformed) > 0:
        pop_list = []
        for k in untransformed:
            cur_rule = new_rules[k]
            for x in transformed:
                y = re.search(fr'(\s|^){x}(\s|$)', cur_rule)
                while y is not None:
                    mat = y.group(0)
                    new_str = ''
                    if re.match(r'\s', mat):
                        new_str += ' '
                    new_str += new_rules[x]
                    if re.search(r'\s$', mat):
                        new_str += ' '
                    cur_rule = cur_rule[:y.span()[0]] + new_str + cur_rule[y.span()[1]:]
                    y = re.search(fr'\s{x}\s|^{x}\s|\s{x}$', cur_rule)
            if re.fullmatch(r'[^0-9]*', cur_rule) is not None:
                pop_list.append(untransformed.index(k))
                if '|' in cur_rule:
                    cur_rule = f'( {cur_rule} )'
                #print((f'{k}:', new_rules[k], '=>', cur_rule))
            new_rules[k] = cur_rule
            
        for j in pop_list[::-1]:
            transformed.append(untransformed.pop(j))

    regex = new_rules['0'].replace(' ', '')
    return regex, new_rules
    

if __name__ == '__main__':
    content = day01.load_data('data19.txt')

    raw_rules = {}
    messages = []

    # find the two rules which only contain either "a" or "b"
    target_dict = {}

    for c in content:
        c = c.split('\n')[0]
        if re.match(r'^\d+:', c):
            (num, entry) = c.split(':')
            my_entry = entry.strip(' ').strip('"')
            raw_rules[num] = my_entry
            if my_entry in ['a', 'b']:
                target_dict[num] = my_entry
        else:
            messages.append(c)

    ## part 1
    regex, new_rules = find_regex_part1(target_dict, raw_rules)
    matches1 = 0
    matched = []
    for m in messages:
        if re.fullmatch(regex, m):
            matches1 += 1
            matched.append(m)
    print(f'Part 1: {matches1}')

    ## part 2
    updates = {'8': '42 | 42 8', 
               '11': '42 31 | 42 11 31'}
    regex31 = new_rules['31'].replace(' ', '')
    regex42 = new_rules['42'].replace(' ', '')
    # this basically means, that
    # rule 8 matches any amount of rule 42 in series
    # rule 11 matches any amount of rule 42 followed by the same amount of rule 31
    # The rules that matches up until now still do, so it should be enough to check the additional rules which match now
    matches2 = matches1
    for m in messages:
        if m in matched:
            continue
        m42 = []
        m31 = []
        # look for matches of rule 42 in m, as beginning of string has to match rule 42 at least once
        temp = m
        ma = re.match(regex42, m)
        while ma is not None:
            m42.append(temp[ma.span()[0]:ma.span()[1]])
            temp = temp[ma.span()[1]:]
            ma = re.match(regex42, temp)
        if len(m42) >= 2: #we need at least once for rule 8 and at least once for rule 31
            ma = re.match(regex31, temp)
            while ma is not None:
                m31.append(temp[ma.span()[0]:ma.span()[1]])
                temp = temp[ma.span()[1]:]
                ma = re.match(regex31, temp)
            if len(temp) == 0:  # full message has been matched
                if len(m31) > 0 and len(m42) > len(m31):
                    matches2 += 1
                    matched.append(m)
    print(f'Part 2: {matches2}')
