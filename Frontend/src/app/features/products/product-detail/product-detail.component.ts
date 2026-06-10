import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.scss'],
})
export class ProductDetailComponent implements OnInit {
  product: any = null;
  loading = true;
  error: string | null = null;
  selectedImage: string | null = null;
  quantity = 1;
  addingToCart = false;
  cartMessage: string | null = null;

  private apiUrl = environment.apiUrl;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.fetchProduct(idParam);
    } else {
      this.error = 'Invalid product ID';
      this.loading = false;
    }
  }

  fetchProduct(id: string): void {
    this.loading = true;
    this.error = null;
    this.http.get<any>(`${this.apiUrl}/products/${id}/`).subscribe({
      next: (data) => {
        this.product = data;
        if (data.images && data.images.length > 0) {
          const primary = data.images.find((img: any) => img.is_primary);
          this.selectedImage = primary ? primary.image : data.images[0].image;
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load product:', err);
        this.error = 'Failed to load product details.';
        this.loading = false;
      },
    });
  }

  selectImage(url: string): void {
    this.selectedImage = url;
  }

  increaseQty(): void {
    if (this.product && this.quantity < this.product.stock_quantity) {
      this.quantity++;
    }
  }

  decreaseQty(): void {
    if (this.quantity > 1) {
      this.quantity--;
    }
  }

  addToCart(): void {
    if (!this.product) return;

    this.addingToCart = true;
    this.cartMessage = null;

    const payload = {
      product_id: this.product.id,
      quantity: this.quantity,
    };

    console.log('Adding to cart:', payload);

    this.http.post<any>(`${this.apiUrl}/cart/`, payload).subscribe({
      next: (res) => {
        console.log('Cart response:', res);
        this.cartMessage = `✓ ${this.product.name} added to cart!`;
        this.addingToCart = false;
        setTimeout(() => (this.cartMessage = null), 4000);
      },
      error: (err) => {
        console.error('Add to cart failed:', err);
        this.cartMessage = '✗ Failed to add to cart. Please try again.';
        this.addingToCart = false;
        setTimeout(() => (this.cartMessage = null), 4000);
      },
    });
  }

  goBack(): void {
    this.router.navigate(['/products']);
  }
}
