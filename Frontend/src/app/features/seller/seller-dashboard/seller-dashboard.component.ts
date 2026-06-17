import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SellerDashboardService, DashboardData } from '../../../core/services/seller-dashboard.service';
import { DashboardStatsComponent } from './components/dashboard-stats/dashboard-stats.component';
import { DashboardChartsComponent } from './components/dashboard-charts/dashboard-charts.component';
import { DashboardRecentOrdersComponent } from './components/dashboard-recent-orders/dashboard-recent-orders.component';
import { DashboardTopProductsComponent } from './components/dashboard-top-products/dashboard-top-products.component';

@Component({
  selector: 'app-seller-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    DashboardStatsComponent,
    DashboardChartsComponent,
    DashboardRecentOrdersComponent,
    DashboardTopProductsComponent
  ],
  templateUrl: './seller-dashboard.component.html',
  styleUrls: ['./seller-dashboard.component.scss'],
})
export class SellerDashboardComponent implements OnInit {
  dashboardData: DashboardData | null = null;
  loading = true;

  constructor(private dashboardService: SellerDashboardService) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.dashboardService.getDashboardData().subscribe({
      next: (data) => {
        this.dashboardData = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Failed to load dashboard data', error);
        this.loading = false;
      }
    });
  }
}
