import day01

if __name__ == '__main__':
    content = day01.load_data('data21.txt')

    ingredients = {}
    allergens = {}
    dishes = {}

    for j, c in enumerate(content):
        (ingr, allerg) = c.split(' (contains ')
        for ing in ingr.split(' '):
            if ing not in ingredients.keys():
                ingredients[ing] = []
            ingredients[ing].append(j)
        for al in allerg.split(')')[0].split(','):
            if al.strip(' ') not in allergens.keys():
                allergens[al.strip(' ')] = []
            allergens[al.strip(' ')].append(j)
        dishes[j] = ingr.split(' ')

    ## part 1
    all_ingr = list(ingredients.keys())
    all_allergens = list(allergens.keys())

    final_allergens = {}
    for a in all_allergens:
        # find shared ingredients
        my_ingr = None
        for dish_num in allergens[a]:
            if my_ingr is None:
                my_ingr = dishes[dish_num][:]
            else:
                my_ingr = [x for x in my_ingr if x in dishes[dish_num]]
        final_allergens[a] = my_ingr

    while any([isinstance(v, list) for v in final_allergens.values()]):
        for k, v in final_allergens.items():
            if isinstance(v, list):
                if len(v) == 1:
                    final_allergens[k] = v[0]
                else:
                    final_allergens[k] = [x for x in v if x not in final_allergens.values()]

    tot = 0
    for i in ingredients.keys():
        if i not in final_allergens.values():
            tot += len(ingredients[i])
    print(f'Part 1: {tot}')

    # part 2
    canonical_dangerous = ''

    for k in sorted(final_allergens.keys()):
        canonical_dangerous += f'{final_allergens[k]},'
    canonical_dangerous = canonical_dangerous[:-1]
    print(f'Part 2: {canonical_dangerous}')