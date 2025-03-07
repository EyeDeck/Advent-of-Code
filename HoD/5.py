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

cat_foods = {k: v for k, v in products_sku.items() if 'Cat Food' in v['desc']}

orders_with_cat_food = [order for order in orders if any(True for item in order['items'] if item['sku'] in cat_foods)]

qty_by_customer = collections.Counter()
for order in orders_with_cat_food:
    items = order['items']

    qty_by_customer[order['customerid']] += sum(item['qty'] for item in items if item['sku'] in cat_foods)

qty_by_customer = {k:v for k,v in qty_by_customer.items() if customers_id[k]['citystatezip'].startswith('Staten Island, NY')}

most_cat_food = max(qty_by_customer.items(), key=lambda x: x[1])

print(customers_id[most_cat_food[0]]['phone'])
