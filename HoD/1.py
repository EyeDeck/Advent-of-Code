import json

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]

# print(customers)
possible = {}
phone_map_rev = {' ': 0, '_,@': 1, 'ABC': 2, 'DEF': 3, 'GHI': 4, 'JKL': 5, 'MNO': 6, 'PQRS': 7, 'TUV': 8, 'WXYZ': 9}
phone_map = {v: set(c for c in k) for k, v in phone_map_rev.items()}

# print(phone_map)

for customer in customers:
    c_name = customer['name'].split()
    if c_name[-1] in {'Jr.', 'I', 'II', 'III', 'IV', 'V'}:
        c_last_name = c_name[-2]
    else:
        c_last_name = c_name[-1]

    # print(c_last_name)
    # phone = [int(c) for c in ''.join(customer['phone'].split('-')[1:])]
    phone = [int(c) for c in ''.join(customer['phone'].split('-'))]
    # print(phone)
    if len(c_last_name) != 10:
        continue
        # possible[customer['id']] = customer

    for i, digit in enumerate(phone):
        # print(c_last_name[i], phone_map[digit])
        if c_last_name[i].upper() not in phone_map[digit]:
            # print('broke on', i, digit, c_last_name[i], phone_map[digit])
            break
    else:
        print(customer)

# print(possible)

for product in products:
    if product['sku'][:3] not in {'TOY', 'DLI', 'PET', 'BKY', 'COL'}:
        print(product)
