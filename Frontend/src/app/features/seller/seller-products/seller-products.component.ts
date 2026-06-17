import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-seller-products',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="glass-placeholder-page">
      <div class="icon">📦</div>
      <h1>My Products</h1>
      <p>Seller products management page - Coming soon</p>
    </div>
  `,
  styles: [
    `
      .glass-placeholder-page {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 60px 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      }
      .glass-placeholder-page .icon {
        font-size: 64px;
        margin-bottom: 24px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
      }
      .glass-placeholder-page h1 {
        font-size: 28px;
        color: white;
        margin: 0 0 16px 0;
        font-weight: 700;
      }
      .glass-placeholder-page p {
        color: #cbd5e1;
        font-size: 16px;
        margin: 0;
      }
    `,
  ],
})
export class SellerProductsComponent {}
