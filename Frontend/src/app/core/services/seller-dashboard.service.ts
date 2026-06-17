import { Injectable } from '@angular/core';
import { Observable, of, delay } from 'rxjs';

export interface StatCard {
  label: string;
  value: string | number;
  icon: string;
  trend?: string;
  color: string;
}

export interface RecentOrder {
  id: number;
  customer: string;
  amount: number;
  status: string;
  date: string;
}

export interface TopProduct {
  name: string;
  sales: number;
  revenue: number;
  image?: string;
}

export interface DashboardData {
  stats: StatCard[];
  recentOrders: RecentOrder[];
  topProducts: TopProduct[];
}

@Injectable({
  providedIn: 'root'
})
export class SellerDashboardService {

  constructor() { }

  getDashboardData(): Observable<DashboardData> {
    // Mock data mimicking an API call
    const data: DashboardData = {
      stats: [
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
      ],
      recentOrders: [
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
      ],
      topProducts: [
        { name: 'Premium Headphones', sales: 342, revenue: 68400 },
        { name: 'Wireless Charger', sales: 289, revenue: 34680 },
        { name: 'Phone Case', sales: 567, revenue: 17010 },
        { name: 'Screen Protector', sales: 892, revenue: 8920 },
        { name: 'USB Cable', sales: 1245, revenue: 12450 },
      ]
    };

    return of(data).pipe(delay(500)); // Simulate network delay
  }
}
