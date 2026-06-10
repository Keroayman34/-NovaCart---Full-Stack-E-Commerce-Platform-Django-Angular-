import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()

user = User.objects.filter(is_superuser=False).first()
if not user:
    user = User.objects.create_user(email="test@example.com", password="password")

client.force_login(user)

print("--- GET CART ---")
res = client.get('/api/cart/')
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("--- POST CART ---")
res = client.post('/api/cart/', data=json.dumps({"product_id": 1, "quantity": 1}), content_type="application/json")
print(res.status_code)
print(json.dumps(res.json(), indent=2))
