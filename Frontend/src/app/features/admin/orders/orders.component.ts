import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { OrdersService, Order } from './orders.service';
import { OrderDetailComponent } from './order-detail/order-detail.component';

@Component({
  selector: 'app-admin-orders',
  standalone: true,
  imports: [CommonModule, FormsModule, OrderDetailComponent],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss'],
})
export class OrdersComponent implements OnInit {
  orders: Order[] = [];
  loading = false;
  errorMessage = '';
  successMessage = '';

  // Pagination
  currentPage = 1;
  totalPages = 1;
  pageNumbers: number[] = [];

  // Filters
  selectedStatus = '';
  searchTerm = '';
  statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'pending', label: 'Pending' },
    { value: 'confirmed', label: 'Confirmed' },
    { value: 'shipped', label: 'Shipped' },
    { value: 'delivered', label: 'Delivered' },
    { value: 'cancelled', label: 'Cancelled' },
  ];

  // Modal
  showDetailModal = false;
  selectedOrder: Order | null = null;
  updateStatusMode = false;
  newStatus = '';

  constructor(private ordersService: OrdersService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(page: number = 1): void {
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.ordersService.getOrders(page, this.selectedStatus, this.searchTerm).subscribe({
      next: (response) => {
        this.orders = response.results;
        this.currentPage = page;
        this.totalPages = Math.ceil(response.count / 10);
        this.generatePageNumbers();
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load orders. Please try again.';
        this.loading = false;
      },
    });
  }

  generatePageNumbers(): void {
    this.pageNumbers = [];
    const maxPagesToShow = 5;
    let startPage = Math.max(1, this.currentPage - 2);
    let endPage = Math.min(this.totalPages, startPage + maxPagesToShow - 1);

    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      this.pageNumbers.push(i);
    }
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.loadOrders(page);
      window.scrollTo(0, 0);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.goToPage(this.currentPage - 1);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.goToPage(this.currentPage + 1);
    }
  }

  onStatusFilterChange(): void {
    this.currentPage = 1;
    this.loadOrders();
  }

  onSearch(): void {
    this.currentPage = 1;
    this.loadOrders();
  }

  resetFilters(): void {
    this.selectedStatus = '';
    this.searchTerm = '';
    this.currentPage = 1;
    this.loadOrders();
  }

  viewOrderDetail(order: Order): void {
    this.selectedOrder = order;
    this.updateStatusMode = false;
    this.newStatus = order.status;
    this.showDetailModal = true;
  }

  enableStatusUpdate(): void {
    this.updateStatusMode = true;
  }

  saveStatusUpdate(): void {
    if (!this.selectedOrder || this.newStatus === this.selectedOrder.status) {
      this.updateStatusMode = false;
      return;
    }

    this.loading = true;
    this.ordersService.updateOrderStatus(this.selectedOrder.id, this.newStatus).subscribe({
      next: (response) => {
        this.successMessage = 'Order status updated successfully!';
        if (this.selectedOrder) {
          this.selectedOrder.status = this.newStatus as any;
        }
        const index = this.orders.findIndex((o) => o.id === this.selectedOrder!.id);
        if (index !== -1) {
          this.orders[index].status = this.newStatus as any;
        }
        this.updateStatusMode = false;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to update order status. Please try again.';
        this.loading = false;
      },
    });
  }

  cancelStatusUpdate(): void {
    this.updateStatusMode = false;
    this.newStatus = this.selectedOrder!.status;
  }

  closeModal(): void {
    this.showDetailModal = false;
    this.selectedOrder = null;
    this.updateStatusMode = false;
  }

  getStatusBadgeClass(status: string): string {
    const baseClass = 'status-badge';
    switch (status) {
      case 'pending':
        return `${baseClass} status-pending`;
      case 'confirmed':
        return `${baseClass} status-confirmed`;
      case 'shipped':
        return `${baseClass} status-shipped`;
      case 'delivered':
        return `${baseClass} status-delivered`;
      case 'cancelled':
        return `${baseClass} status-cancelled`;
      default:
        return baseClass;
    }
  }

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      pending: 'Pending',
      confirmed: 'Confirmed',
      shipped: 'Shipped',
      delivered: 'Delivered',
      cancelled: 'Cancelled',
    };
    return labels[status] || status;
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  }
}
