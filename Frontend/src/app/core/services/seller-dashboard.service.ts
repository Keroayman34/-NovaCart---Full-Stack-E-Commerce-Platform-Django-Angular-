import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

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
  private apiUrl = `${environment.apiUrl}/sellers/dashboard/`;

  constructor(private http: HttpClient) {}

  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(this.apiUrl);
  }
}
