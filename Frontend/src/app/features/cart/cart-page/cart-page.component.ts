import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-cart-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './cart-page.component.html',
  styleUrls: ['./cart-page.component.scss'],
})
export class CartPageComponent implements OnInit {
  cart: any = null;
  loading = true;
  error: string | null = null;
  updating = false;

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.loading = true;
    this.error = null;
    this.http.get<any>(`${this.apiUrl}/cart/`).subscribe({
      next: (data) => {
        this.cart = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load cart:', err);
        this.error = 'Failed to load cart.';
        this.loading = false;
      },
    });
  }

  updateQuantity(itemId: number, newQty: number): void {
    if (newQty < 1) return;
    this.updating = true;
    this.http.patch<any>(`${this.apiUrl}/cart/${itemId}/`, { quantity: newQty }).subscribe({
      next: (data) => {
        this.cart = data;
        this.updating = false;
      },
      error: (err) => {
        console.error('Failed to update quantity:', err);
        this.updating = false;
      },
    });
  }

  removeItem(itemId: number): void {
    this.updating = true;
    this.http.delete<any>(`${this.apiUrl}/cart/${itemId}/`).subscribe({
      next: () => {
        this.loadCart();
        this.updating = false;
      },
      error: (err) => {
        console.error('Failed to remove item:', err);
        this.updating = false;
      },
    });
  }

  clearCart(): void {
    this.updating = true;
    this.http.delete<any>(`${this.apiUrl}/cart/clear/`).subscribe({
      next: () => {
        this.loadCart();
        this.updating = false;
      },
      error: (err) => {
        console.error('Failed to clear cart:', err);
        this.updating = false;
      },
    });
  }

  proceedToCheckout(): void {
    this.router.navigate(['/checkout']);
  }

  get hasItems(): boolean {
    return this.cart?.items?.length > 0;
  }
}
