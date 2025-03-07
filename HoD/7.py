import collections
import json
from collections import defaultdict

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]
    customers_id = {c['customerid']: c for c in customers}

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]
    orders_id = {o['orderid']: o for o in orders}

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]
    products_sku = {p['sku']: p for p in products}

woman = 4167

orders_by_woman = []

for order_id, order in orders_id.items():
    customer_id = order['customerid']
    if customer_id != woman or order['ordered'] != order['shipped']:
        continue

    orders_by_woman.append(order)


def get_desc(sku):
    desc = products_sku[sku]['desc'].split()
    return ' '.join(desc[:-1]), desc[-1][1:-1]


collectibles = []
for order in orders_by_woman:
    for item in order['items']:
        if not item['sku'].startswith('COL'):
            continue
        if item['qty'] > 1:
            continue
        collectibles.append((order['ordered'].split()[0], item['sku'], get_desc(item['sku'])))
        print(order)
# print(collectibles)
print(collectibles)

days = [item[0] for item in collectibles]
collectible_types = [item[2][0] for item in collectibles]
collectible_skus = [item[1] for item in collectibles]

# print(days, collectible_types, collectible_skus)

# {"sku": "COL0041", "desc": "Noah's Ark Model (HO Scale)", "wholesale_cost": 2487.35, "dims_cm": [7.2, 4.3, 0.4]}

similar = defaultdict(set)
for sku, product in products_sku.items():
    if not sku.startswith('COL'):
        continue
    item, color = get_desc(sku)
    if item in collectible_types:
        similar[item].add(sku)
    # print(sku, item, color)

for thing in similar.items():
    print(thing)

for order_id, order in orders_id.items():
    if order['customerid'] == woman or order['ordered'] != order['shipped']:
        continue
    day_a = order['ordered'].split()[0]
    for day_b, type, sku_b in zip(days, collectible_types, collectible_skus):
        if day_a != day_b:
            continue
        for item in order['items']:
            sku_a = item['sku']
            if not sku_a.startswith('COL'):
                continue
            it, c = get_desc(sku_a)
            if sku_a != sku_b and sku_a in similar[it]:
                print(order)