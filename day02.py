import re
import day01

def split_entry(a_entry):
    """ split line in text input into password policy (rule) and password (word) """
    # a_rule is of the form X-Y z, where X and Y are numbers and z and arbitrary character
    rule = a_entry.split(':')[0].strip(' ')
    word = a_entry.split(':')[1].strip(' ')
    (my_range, char) = rule.split(' ')
    (val1, val2) = (map(int, my_range.split('-')))

    return val1, val2, char, word

def is_valid_rule1(a_entry):
    (my_min, my_max, char, word) = split_entry(a_entry)
    cnts = len(re.findall(char, word))
    return my_min <= cnts <= my_max

def is_valid_rule2(a_entry):
    (idx1, idx2, char, word) = split_entry(a_entry)
    char1_match = word[idx1-1] == char
    char2_match = word[idx2-1] == char
    return (char1_match or char2_match) and not (char1_match and char2_match)

if __name__ == '__main__':
    content = day01.load_data('data02.txt')

    ## part 1
    valids = list(filter(is_valid_rule1, content))
    print(f'Number of valid passwords (rule 1): {len(valids)}')

    ## part 2
    valids = list(filter(is_valid_rule2, content))
    print(f'Number of valid passwords (rule 2): {len(valids)}')
