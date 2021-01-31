import re
import day01

def get_passport_list(a_content):
    # split up ugly entries into list of passport strings
    pports = []
    active_pport = ''
    for c in a_content:
        if len(c) == 0:
            pports.append(active_pport)
            active_pport = ''
        else:
            active_pport += c.replace(' ', '')
    if active_pport != '':
        pports.append(active_pport)
    return pports

def is_valid_rule1(a_entries):
    must_have = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] # , 'cid' is optional!
    is_okay = True
    for mh in must_have:
        m = re.search(f'{mh}:', a_entries)
        is_okay = is_okay and m is not None
        if not is_okay:
            break
    return is_okay

def is_valid_rule2(a_entries):
    must_have = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] # , 'cid' is optional!
    # use part one to rule out the ones with missing entires from the get-go
    entry_okay = is_valid_rule1(a_entries)
    if entry_okay:
        # dump all into dictionary
        idxs = sorted(map(a_entries.index, must_have))
        # check for optional cid, it has to be split if present
        if 'cid:' in a_entries:
            idxs.append(a_entries.index('cid'))
            idxs = sorted(idxs)
        my_dict = {}
        for j in range(len(idxs)):
            if j < len(idxs) - 1:
                v = a_entries[idxs[j]:idxs[j+1]]
            else:
                v = a_entries[idxs[j]:]
            my_dict[v.split(':')[0]] = v.split(':')[1]

        for mh in must_have:
            my_val_str = my_dict[mh]
            if 'yr' in mh:
                # turn into year - 4 digits followed by a letter or the end of the string
                re_search = re.match(fr'^[1-2]([0-9]){{3}}$', my_val_str)
                if re_search is not None:
                    yr = int(re_search.group(0))
                    if mh == 'byr':
                        entry_okay = 1920 <= yr <= 2002
                    elif mh == 'iyr':
                        entry_okay = 2010 <= yr <= 2020
                    elif mh == 'eyr':
                        entry_okay = 2020 <= yr <= 2030
                else:
                    entry_okay = False
            elif mh == 'hgt':
                # metric
                re_search = re.search(r'1[5-9][0-9]cm', my_val_str)
                if re_search is not None:
                    height = int(re_search.group(0).strip('cm'))
                    entry_okay = 150 <= height <= 193
                # imperial
                else:
                    re_search = re.search(r'[5-7][0-9]in', my_val_str)
                    if re_search is not None:
                        height = int(re_search.group(0).strip('in'))
                        entry_okay = 59 <= height <= 76
                    else:
                        entry_okay = False
            elif mh == 'hcl':
                entry_okay = re.search(r'^#([a-z0-9]){6}$', my_val_str) is not None
            elif mh == 'ecl':
                entry_okay = my_val_str in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
            elif mh == 'pid':
                entry_okay = re.search(r'^([0-9]){9}$', my_val_str) is not None
            else:
                pass  # do not check 'cid'
            if not entry_okay:
                break
    
    return entry_okay                    

if __name__ == "__main__":
    content = day01.load_data('data04.txt')
    passports = get_passport_list(content)

    ## part 1
    valids = list(filter(is_valid_rule1, passports))
    print(f'Found {len(valids)} valid passports (part 1)')

    ## part 2
    valids = list(filter(is_valid_rule2, passports))
    print(f'Found {len(valids)} valid passports (part 2)')
