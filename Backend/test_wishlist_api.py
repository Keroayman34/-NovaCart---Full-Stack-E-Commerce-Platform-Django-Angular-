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

print("--- GET WISHLIST ---")
res = client.get('/api/wishlist/')
print(res.status_code)
print(json.dumps(res.json(), indent=2))
