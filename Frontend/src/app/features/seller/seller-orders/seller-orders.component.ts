import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SellerOrderService, SellerOrder } from '../../../core/services/seller-order.service';

@Component({
  selector: 'app-seller-orders',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './seller-orders.component.html',
  styleUrls: ['./seller-orders.component.scss']
})
export class SellerOrdersComponent implements OnInit {
  orders: SellerOrder[] = [];
  loading = true;
  error = '';
  updatingOrderId: number | null = null;
  
  statusOptions = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'];

  constructor(private sellerOrderService: SellerOrderService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(): void {
    this.loading = true;
    this.sellerOrderService.getOrders().subscribe({
      next: (data) => {
        this.orders = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading orders', err);
        this.error = 'Failed to load orders.';
        this.loading = false;
      }
    });
  }

  updateStatus(order: SellerOrder, event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    const newStatus = selectElement.value;
    
    if (order.status === newStatus) return;
    
    this.updatingOrderId = order.id;
    this.sellerOrderService.updateOrderStatus(order.id, newStatus).subscribe({
      next: (res) => {
        order.status = newStatus;
        this.updatingOrderId = null;
      },
      error: (err) => {
        console.error('Failed to update status', err);
        // Revert select visually if failed
        selectElement.value = order.status;
        this.updatingOrderId = null;
        alert('Failed to update order status. Please try again.');
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }
}
// Trigger recompile
