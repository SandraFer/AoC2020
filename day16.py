import day01

def is_valid(a_value, a_rules):
    val = False
    for _, v in a_rules.items():
        if not val:
            ok = False
            for vi in v:
                ok = vi[0] <= a_value <= vi[1]
                if ok:
                    break
            val = ok
    return val

def fail_filter(a_rules):
    def my_filter(a_value):
        return not is_valid(a_value, a_rules)
    return my_filter

def get_ticket_error_rate(a_ticket, a_rules):
    my_filt = fail_filter(a_rules)
    not_ok = list(filter(my_filt, a_ticket))
    return sum(not_ok)

def valid_ticket(a_ticket, a_rules):
    my_filt = fail_filter(a_rules)
    not_ok = list(filter(my_filt, a_ticket))
    return sum(not_ok) == 0

if __name__ == '__main__':
    content = day01.load_data('data16.txt')

    my_ticket = None
    nearby_tickets = []
    rules = {}

    cat = 'rules'

    for c in content:
        if len(c) > 0:
            if 'your ticket' in c:
                cat = 'mine'
                continue
            elif 'nearby tickets' in c:
                cat = 'nearby'
                continue
            if cat == 'rules':
                rulename = c.split(':')[0]
                rulecontent = []
                for x in c.split(':')[1].split(' or '):
                    rulecontent.append([int(y) for y in x.split('-')])
                rules[rulename] = rulecontent
            elif cat == 'mine':
                my_ticket = list(map(int, c.split(',')))
            else:
                nearby_tickets.append(list(map(int, c.split(','))))

    all_tickets = nearby_tickets[:]
    all_tickets.append(my_ticket)

    ## part 1 
    error_rate = 0
    for t in all_tickets:
        err = get_ticket_error_rate(t, rules)
        error_rate += err
    print(f'Part 1: {error_rate}')

    ## part 2
    keepers = list(filter(lambda x: valid_ticket(x, rules), all_tickets))
    location_values = dict((i, [k[i] for k in keepers]) for i in range(len(rules.keys())))
    rules_positions_cand = dict((k, []) for k in rules.keys())

    for j, ticket in location_values.items():
        # find rule where all values in v are okay
        # treat v like a ticket to re-use same function
        for k, v in rules.items():
            loop_rule = {k: v}
            x = valid_ticket(ticket, loop_rule)
            if x:
                rules_positions_cand[k].append(j)

    # sort by minimun number of candidates
    srt = [(k, v) for k, v in sorted(rules_positions_cand.items(), key=lambda x: len(x[1]))]
    final_dict = {}
    for k, v in srt:
        cand = [x for x in v if x not in final_dict.values()]
        if len(cand) == 1:
            final_dict[k] = cand[0]
    tot = 1
    for k, v in final_dict.items():
        if 'departure ' in k:
            tot *= my_ticket[v]
    print(f'Part 2: {tot}')
