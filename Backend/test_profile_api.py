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

print("--- GET PROFILE ---")
res = client.get('/api/profile/')
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("--- PATCH PROFILE ---")
res = client.patch('/api/profile/', data=json.dumps({"phone": "9876543210"}), content_type="application/json")
print(res.status_code)
print(json.dumps(res.json(), indent=2))
