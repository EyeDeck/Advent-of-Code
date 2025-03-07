import collections
import json

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]
    customers_id = {c['customerid']: c for c in customers}

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]
    orders_id = {o['orderid']: o for o in orders}

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]
    products_sku = {p['sku']: p for p in products}

# {"orderid": 214202, "customerid": 2824, "ordered": "2022-12-16 17:46:36",
# "shipped": "2022-12-16 17:46:36",
# "items": [{"sku": "TOY8955", "qty": 1, "unit_price": 5.26},
# {"sku": "PET3882", "qty": 1, "unit_price": 1.03},
# {"sku": "COL1659", "qty": 1, "unit_price": 42.91}],
# "total": 49.199999999999996}

total_orders_by_customer = collections.defaultdict(dict)
profit_by_customer = collections.Counter()
for order_id, order in orders_id.items():
    customer_id = order['customerid']
    for item in order['items']:
        sku = item['sku']
        qty = item['qty']
        p = item['unit_price']
        d = total_orders_by_customer[customer_id]
        if sku not in d:
            d[sku] = collections.Counter()
        d[sku][p] += qty

        profit = p - products_sku[sku]['wholesale_cost']
        profit_by_customer[customer_id] += profit

worst_customer = min(profit_by_customer.items(), key=lambda x:x[1])[0]
print(customers_id[worst_customer]['phone'])

# for c, o in total_orders_by_customer.items():
#     print(c,o)