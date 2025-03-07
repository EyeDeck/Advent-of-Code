import collections
import json

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]
    customers_id = {c['customerid']: c for c in customers}

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]
    products_sku = {p['sku']: p for p in products}

first_by_day = {}
for order in orders:
    if order['shipped'] != order['ordered']:
        continue

    day, time = order['ordered'].split()
    if int(time.split(':')[0]) >= 9:
        continue

    if not any(product['sku'].startswith('BKY') for product in order['items']):
        continue

    if day in first_by_day:
        continue

    first_by_day[day] = order

first_orderers = collections.Counter(o['customerid'] for o in first_by_day.values())

top_early_orderer = max(first_orderers.items(), key=lambda x: x[1])

print(customers_id[top_early_orderer[0]]['phone'])
