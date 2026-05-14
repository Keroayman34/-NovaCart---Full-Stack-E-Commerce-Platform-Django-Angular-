import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface StatCard {
  label: string;
  value: string | number;
  icon: string;
  trend?: string;
  color: string;
}

interface RecentOrder {
  id: number;
  customer: string;
  amount: number;
  status: string;
  date: string;
}

interface TopProduct {
  name: string;
  sales: number;
  revenue: number;
  image?: string;
}

@Component({
  selector: 'app-seller-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './seller-dashboard.component.html',
  styleUrls: ['./seller-dashboard.component.scss'],
})
export class SellerDashboardComponent implements OnInit {
  stats: StatCard[] = [];
  recentOrders: RecentOrder[] = [];
  topProducts: TopProduct[] = [];
  loading = true;

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    // In a real app, this would fetch data from backend APIs
    // For now, using mock data
    setTimeout(() => {
      this.stats = [
        {
          label: 'Total Sales',
          value: '₹45,230',
          icon: '💰',
          trend: '+12.5%',
          color: 'blue',
        },
        {
          label: 'Total Orders',
          value: '156',
          icon: '📦',
          trend: '+8.2%',
          color: 'green',
        },
        {
          label: 'Active Products',
          value: '42',
          icon: '📊',
          trend: '+5.1%',
          color: 'purple',
        },
        {
          label: 'Avg Rating',
          value: '4.8',
          icon: '⭐',
          trend: '+0.3',
          color: 'orange',
        },
      ];

      this.recentOrders = [
        {
          id: 1001,
          customer: 'John Doe',
          amount: 2500,
          status: 'delivered',
          date: '2 hours ago',
        },
        {
          id: 1002,
          customer: 'Jane Smith',
          amount: 1850,
          status: 'shipped',
          date: '5 hours ago',
        },
        {
          id: 1003,
          customer: 'Mike Johnson',
          amount: 3200,
          status: 'processing',
          date: '1 day ago',
        },
        {
          id: 1004,
          customer: 'Sarah Williams',
          amount: 1500,
          status: 'pending',
          date: '2 days ago',
        },
        {
          id: 1005,
          customer: 'Robert Brown',
          amount: 4100,
          status: 'delivered',
          date: '3 days ago',
        },
      ];

      this.topProducts = [
        { name: 'Premium Headphones', sales: 342, revenue: 68400 },
        { name: 'Wireless Charger', sales: 289, revenue: 34680 },
        { name: 'Phone Case', sales: 567, revenue: 17010 },
        { name: 'Screen Protector', sales: 892, revenue: 8920 },
        { name: 'USB Cable', sales: 1245, revenue: 12450 },
      ];

      this.loading = false;
    }, 500);
  }

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

  getStatCardClass(stat: StatCard): string {
    return `stat-card stat-${stat.color}`;
  }
}
