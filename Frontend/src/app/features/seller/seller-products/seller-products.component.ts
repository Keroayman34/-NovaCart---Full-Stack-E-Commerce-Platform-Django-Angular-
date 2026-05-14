import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-seller-products',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="placeholder-page">
      <h1>My Products</h1>
      <p>Seller products management page - Coming soon</p>
    </div>
  `,
  styles: [
    `
      .placeholder-page {
        background: white;
        border-radius: 8px;
        padding: 40px 20px;
        text-align: center;
        border: 1px solid #e5e7eb;

        h1 {
          font-size: 24px;
          color: #333;
          margin: 0 0 12px 0;
        }

        p {
          color: #666;
          margin: 0;
        }
      }
    `,
  ],
})
export class SellerProductsComponent {}
