import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage

def seed_images():
    products = Product.objects.all()
    count = products.count()
    print(f"Found {count} products. Adding images...")

    for index, product in enumerate(products, 1):
        if product.images.exists():
            print(f"[{index}/{count}] Product {product.id} already has an image. Skipping.")
            continue

        print(f"[{index}/{count}] Downloading image for product {product.id}: {product.name}")
        try:
            # Add a random seed to get different images for each product
            image_url = f"https://picsum.photos/seed/{product.id}/600/400"
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
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
