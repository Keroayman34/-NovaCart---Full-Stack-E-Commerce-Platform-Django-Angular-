import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Order } from '../orders.service';

@Component({
  selector: 'app-order-detail',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './order-detail.component.html',
  styleUrls: ['./order-detail.component.scss'],
})
export class OrderDetailComponent {
  @Input() order!: Order;
  @Input() updateStatusMode = false;
  @Input() newStatus = '';
  @Output() enableStatusUpdate = new EventEmitter<void>();
  @Output() statusUpdated = new EventEmitter<void>();
  @Output() statusUpdateCancelled = new EventEmitter<void>();
  @Output() closeModal = new EventEmitter<void>();
  @Output() statusChanged = new EventEmitter<string>();

  statusOptions = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'];

  onEnableStatusUpdate(): void {
    this.enableStatusUpdate.emit();
  }

  onStatusUpdated(): void {
    this.statusUpdated.emit();
  }

  onStatusUpdateCancelled(): void {
    this.statusUpdateCancelled.emit();
  }

  onCloseModal(): void {
    this.closeModal.emit();
  }

  onStatusChange(status: string): void {
    this.statusChanged.emit(status);
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
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  }
}
