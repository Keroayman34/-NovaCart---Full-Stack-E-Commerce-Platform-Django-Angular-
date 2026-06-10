import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  cart: any = null;
  loading = true;
  placing = false;
  error: string | null = null;
  success: string | null = null;

  address = '';

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.loading = true;
    this.http.get<any>(`${this.apiUrl}/cart/`).subscribe({
      next: (data) => {
        this.cart = data;
        this.loading = false;
        if (!data.items || data.items.length === 0) {
          this.error = 'Your cart is empty. Add some products first.';
        }
      },
      error: () => {
        this.error = 'Failed to load cart.';
        this.loading = false;
      },
    });
  }

  placeOrder(): void {
    if (!this.address.trim()) {
      this.error = 'Please enter a shipping address.';
      return;
    }
    if (this.placing) return;

    this.placing = true;
    this.error = null;

    this.http.post<any>(`${this.apiUrl}/orders/`, { address: this.address }).subscribe({
      next: (order) => {
        this.success = `Order #${order.id} placed successfully!`;
        this.placing = false;
        setTimeout(() => {
          this.router.navigate(['/profile/orders']);
        }, 2000);
      },
      error: (err) => {
        console.error('Order failed:', err);
        const msg = err.error?.detail || err.error?.non_field_errors?.[0] || err.error?.address?.[0] || 'Failed to place order.';
        this.error = typeof msg === 'string' ? msg : JSON.stringify(msg);
        this.placing = false;
      },
    });
  }

  get hasItems(): boolean {
    return this.cart?.items?.length > 0;
  }
}
