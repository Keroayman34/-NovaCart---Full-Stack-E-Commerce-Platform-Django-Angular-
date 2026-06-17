import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecentOrder } from '../../../../../core/services/seller-dashboard.service';

@Component({
  selector: 'app-dashboard-recent-orders',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-recent-orders.component.html',
  styleUrls: ['./dashboard-recent-orders.component.scss']
})
export class DashboardRecentOrdersComponent {
  @Input() orders: RecentOrder[] = [];

  getStatusBadgeClass(status: string): string {
    const baseClass = 'status-badge';
    switch (status) {
      case 'pending':
        return `${baseClass} status-pending`;
      case 'processing':
        return `${baseClass} status-processing`;
      case 'shipped':
        return `${baseClass} status-shipped`;
      case 'delivered':
        return `${baseClass} status-delivered`;
      default:
        return baseClass;
    }
  }

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      pending: 'Pending',
      processing: 'Processing',
      shipped: 'Shipped',
      delivered: 'Delivered',
    };
    return labels[status] || status;
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  }
}
