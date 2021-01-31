import re
import day01

def makefilter(a_type):
    def myfilter(x):
        return a_type in x[1]
    return myfilter

def look_for_bag(rules, bag):
    next_trgt_list = []
    contains_target = []
    next_target = bag
    while next_target is not None:
        f = makefilter(next_target)
        contain_target_loop = [x for x in list(filter(f, rules.items()))]
        contain_target_loop = [x[0] for x in contain_target_loop if x[0] not in contains_target]
        contains_target += [x for x in contain_target_loop]
        next_trgt_list += [x for x in contain_target_loop]
        try:
            next_target = next_trgt_list.pop(0)
        except IndexError:
            next_target = None
    return contains_target

def search_inside_bags(rules, trgt):
    my_contents = rules[trgt]
    tot = 1
    for k, v in my_contents.items():
        tot += v * search_inside_bags(rules, k)
    return tot

if __name__ == '__main__':
    content = day01.load_data('data07.txt')

    # put all rules in dictionary
    rulebook = {}
    regex = r'^([a-z]* [a-z]*) bags contain (.*)$'
    regex_empty = r'^([a-z]* [a-z]*) bags contain no other bags.$'
    for c in content:
        m = re.match(regex_empty, c)
        if m is None:
            m = re.match(regex, c)
            rulebook[m.group(1)] = {}
            regex_inner = r'(\d [a-z]* [a-z]*) bags?'
            fa = re.findall(regex_inner, c.split('bags contain ')[1])
            for ff in fa:
                cnt = int(ff.split(' ')[0])
                name = ' '.join(ff.split(' ')[1:])
                rulebook[m.group(1)][name] = cnt
        else:
            rulebook[m.group(1)] = {}
            
    target = 'shiny gold'

    ## part 1
    contain_shiny_gold = look_for_bag(rulebook, target)
    print(f'Part 1: {len(contain_shiny_gold)} bags can contain a {target} bag.')

    ## part 2
    tot = search_inside_bags(rulebook, target) - 1  # dont count the shiny gold one!!!
    print(f'Part 2: One {target} bag has to contain {tot} other bags!')
