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


items_by_customer = defaultdict(set)
for order in orders:
    id = order['customerid']
    for item in order['items']:
        sku = item['sku']
        if sku.startswith('COL'):
            items_by_customer[id].add(sku)

most_cols = max(items_by_customer.items(), key=lambda x:len(x[1]))[0]

print(customers_id[most_cols]['phone'])