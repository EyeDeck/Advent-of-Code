import json

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]
    customers_id = {c['customerid']: c for c in customers}

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]
    products_sku = {p['sku']:p for p in products}



# print(phone_map)

# for customer in customers:
#     c_name = customer['name'].split()
#     if c_name[-1] in {'Jr.', 'I', 'II', 'III', 'IV', 'V'}:
#         c_last_name = c_name[-2]
#     else:
#         c_last_name = c_name[-1]
#
#     # print(c_last_name)
#     # phone = [int(c) for c in ''.join(customer['phone'].split('-')[1:])]
#     phone = [int(c) for c in ''.join(customer['phone'].split('-'))]
#     # print(phone)
#     if len(c_last_name) != 10:
#         continue
#         # possible[customer['id']] = customer
#
#     for i, digit in enumerate(phone):
#         # print(c_last_name[i], phone_map[digit])
#         if c_last_name[i].upper() not in phone_map[digit]:
#             # print('broke on', i, digit, c_last_name[i], phone_map[digit])
#             break
#     else:
#         print(customer)

# print(possible)

cleaner = None
for product in products:
    if product['sku'][:3] not in {'TOY', 'DLI', 'PET', 'BKY', 'COL'}:
        cleaner = product['sku']
assert cleaner

def has_SKU(order, sku):
    for item in order['items']:
        if item['sku'] == sku:
            return True
    return False

with_cleaner = [order for order in orders if has_SKU(order, cleaner)]

# print(with_cleaner)

for order in orders:
    if not has_SKU(order, cleaner):
        continue

    ordered = order['ordered']
    if ordered.split('-')[0] != '2017':
        continue

    c_id = order['customerid']
    customer = customers_id[c_id]
    c_name = customer['name'].split()
    if c_name[-1] in {'Jr.', 'I', 'II', 'III', 'IV', 'V'}:
        c_last_name = c_name[-2]
    else:
        c_last_name = c_name[-1]
    c_first_name = c_name[0]
    # print(c_first_name, c_last_name)
    if c_first_name[0] != 'J' or c_last_name[0] != 'P':
        continue

    print(f'{c_id}: {' '.join(c_name)} {customer['phone']}')
    for item in order['items']:
        print('\t', products_sku[item['sku']]['desc'])

