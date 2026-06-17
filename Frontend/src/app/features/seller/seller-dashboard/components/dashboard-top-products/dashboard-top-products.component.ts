import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopProduct } from '../../../../../core/services/seller-dashboard.service';

@Component({
  selector: 'app-dashboard-top-products',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-top-products.component.html',
  styleUrls: ['./dashboard-top-products.component.scss']
})
export class DashboardTopProductsComponent {
  @Input() products: TopProduct[] = [];

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  }
}
