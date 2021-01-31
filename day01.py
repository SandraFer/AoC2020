def load_data(filename):
    """ load puzzle data """
    with open(filename, 'r') as f1:
        content = [c.strip('\n') for c in f1.readlines()]
    return content

def lte_filter_val(a_val):
    """ filter all elements which are <= a_val """
    def lte_filter(x):
        return x <= a_val
    return lte_filter

def find_pair(a_target, a_content, a_skip=None):
    """ find two numbers in list whose sum equals a_target """
    numbers = sorted(list(map(int, a_content)))
    
    # for triple solution: don't pick the same entry twice
    if a_skip is not None:
        numbers.pop(a_skip)
    
    found_pair = False
    while not found_pair and len(numbers) > 0:
        val1 = numbers[0]
        val2 = a_target - val1
        found_pair =  val2 in numbers

        if not found_pair:
            my_filter = lte_filter_val(val2)
            # discard val1 and all elements larger than val2
            numbers = list(filter(my_filter, numbers[1:]))
    if found_pair: # check value
        assert val1 + val2 == a_target, f'Got wrong sum of {val1 + val2} instead of {a_target}'
    return found_pair, val1, val2
    

if __name__ == '__main__':
    content = load_data('data01.txt')

    expense_report = []
    target = 2020

    ## part 1
    (_, my_val1, my_val2) = find_pair(target, content)
    print(f'Solution part 1: {my_val1 * my_val2}')

    ## part 2
    found_triplet = False
    expense_report_outer = sorted(list(map(int, content)))
    idx_outer = 0
    while not found_triplet:
        my_val0 = expense_report_outer[idx_outer]
        (found, my_val1, my_val2) = find_pair(target-my_val0, content, a_skip=idx_outer)
        if found:
            found_triplet = True
        else:
            idx_outer += 1
    if found_triplet:
        print(f'Solution part 2: {my_val1 * my_val2 * my_val0}')
