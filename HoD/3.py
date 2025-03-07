import heapq
import json
import math

with open('noahs-customers.jsonl') as file:
    customers = [json.loads(line) for line in file.readlines()]
    customers_id = {c['customerid']: c for c in customers}

with open('noahs-orders.jsonl') as file:
    orders = [json.loads(line) for line in file.readlines()]

with open('noahs-products.jsonl') as file:
    products = [json.loads(line) for line in file.readlines()]
    products_sku = {p['sku']:p for p in products}


jp = customers_id[1475]

candidates = []
for customer in customers:
    y,m,d = [int(i) for i in customer['birthdate'].split('-')]
    if y % 12 != 7:
        continue
    if m == 6 and d > 21 or m == 7 and d <= 22:
        dist = math.sqrt((jp['lat'] - customer['lat'])**2 + (jp['long'] - customer['long'])**2)
        heapq.heappush(candidates, (dist, customer))

print(heapq.heappop(candidates)[1]['phone'])