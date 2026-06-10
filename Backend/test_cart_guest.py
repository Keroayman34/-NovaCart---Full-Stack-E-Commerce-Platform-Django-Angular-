import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test.client import Client

client = Client()

print("--- POST CART AS GUEST ---")
res = client.post('/api/cart/', data=json.dumps({"product_id": 1, "quantity": 1}), content_type="application/json")
print("STATUS:", res.status_code)
try:
    print(json.dumps(res.json(), indent=2))
except:
    print(res.content)
