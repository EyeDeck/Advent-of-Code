import sys
from collections import *


def p1():
    recipes = []
    all_allerg = set()
    all_ingr = set()
    for line in data:
        ingr, allerg = line.split('(contains')
        ingr = set(ingr.strip().split(' '))
        allerg = set(allerg.strip(')').replace(',', '').strip(' ').split(' '))

        all_allerg.update(allerg)
        all_ingr.update(ingr)

        recipes.append([ingr, allerg])

        # print(ingr, '\n', allerg)
    # print(recipes)
    # print('all ingr:', all_ingr)
    # print('all allerg:', all_allerg)

    might_contain = defaultdict(set)
    known_allergens = {}

    for ingr, allerg in recipes:
        for a in allerg:
            for i in ingr:
                might_contain[a].add(i)

    # print('\nmight_contain')
    # for k, v in might_contain.items():
    #     print(k, v)

    pared = {}
    while len(might_contain) > 0:
        for allerg in all_allerg:
            in_all = all_ingr.copy()
            for i, a in recipes:
                if allerg in a:
                    in_all = in_all.intersection(i)
            pared[allerg] = in_all

        for k, v in pared.items():
            print(k, v)
        print('')

        found_allergen = min(pared, key=lambda key: len(pared[key]))
        found_ingr = pared[found_allergen].pop()
        known_allergens[found_allergen] = found_ingr

        # print(found_allergen, found_ingr)

        del might_contain[found_allergen]
        del pared[found_allergen]
        all_allerg.remove(found_allergen)
        all_ingr.remove(found_ingr)
        # print('all ingr:', all_ingr)
        # print('all allerg:', all_allerg)
        # input()
        pass

    ct = 0
    for ingr in all_ingr:
        for recipe, _ in recipes:
            if ingr in recipe:
                ct +=1

    part1 = ct
    # print(known_allergens)
    part2 = ''
    for key in sorted(known_allergens.keys()):
        part2 += known_allergens[key] + ','
    part2 = part2.strip(',')
    # print(part2)
    return part1, part2

def p2():
    return None


f = 'dx.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

pt1, pt2 = p1()
print(f'part1: {pt1}')
print(f'part2: {pt2}')
