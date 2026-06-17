import os
import django
import urllib.request
import urllib.parse
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage

def seed_images():
    products = Product.objects.all()
    count = products.count()
    print(f"Found {count} products. Re-generating images...")

    # Clear existing images
    ProductImage.objects.all().delete()

    for index, product in enumerate(products, 1):
        print(f"[{index}/{count}] Downloading image for product {product.id}: {product.name}")
        try:
            # High-quality curated Unsplash IDs mapped to keywords
            IMAGE_MAP = {
                'iphone': '1510557880182-3d4d3cba35a5',
                'samsung': '1610945265064-32af161606b8',
                'macbook': '1517336714731-489689fd1ca8',
                'ipad': '1544244015-01c1c1fce81d',
                'headphones': '1505740420928-5e560c06d30e',
                'hub': '1587202372616-98925bbd337c',
                'keyboard': '1595225476474-87563907a212',
                'mouse': '1527814050087-179f0011abcc',
                'webcam': '1587829749591-9e237fb571b0',
                'watch': '1508685096489-7aacd43bd3b1',
                'jacket': '1551028719-00167b16eac5',
                'running': '1542291026-7eec264c27ff',
                'backpack': '1553062407-98eeb64c6a62',
                'coat': '1539533262946-bdf8b5ba8900',
                'jeans': '1542272604-787c3835535d',
                'shoes': '1595950653106-6c9ebd61f561',
                'tee': '1521572163474-6864f9cf17ab',
                'sweater': '1610652492081-37f0170a4ed3',
                'table': '1533090161767-e6ffed986c88',
                'chair': '1505843490538-5133c6c7d0e1',
                'lamp': '1513506003901-1e6a229e9d15',
                'bookshelf': '1507722770857-e6ccba7b6e92',
                'treadmill': '1534438327276-14e5300c3a48',
                'bands': '1598289431512-b2ce1b1ffcc7',
                'bicycle': '1485965120184-e220f721d03e',
                'python': '1526379095098-d400fd0bf935',
                'code': '1498050108023-c5249f4df085',
                'moisturizer': '1556228578-0d85b1a4d571',
                'lipstick': '1586495777744-4413f21062fa',
                'board': '1610890716175-31a8e2949ffb',
                'puzzle': '1580211103759-db3cbdb7f012'
            }

            photo_id = '1505740420928-5e560c06d30e' # fallback
            name_lower = product.name.lower()
            for key, val in IMAGE_MAP.items():
                if key in name_lower:
                    photo_id = val
                    break

            image_url = f"https://images.unsplash.com/photo-{photo_id}?w=600&h=400&fit=crop"
            
            # Download image
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                image_content = response.read()

            image_name = f"product_{product.id}.jpg"
            
            # Create ProductImage
            product_image = ProductImage(
                product=product,
                alt_text=product.name,
                is_primary=True
            )
            product_image.image.save(image_name, ContentFile(image_content), save=True)
            print(f"  -> Successfully added image.")
        except Exception as e:
            print(f"  -> Failed to add image: {e}")

if __name__ == '__main__':
    seed_images()
