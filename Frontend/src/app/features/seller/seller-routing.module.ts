import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SellerLayoutComponent } from './seller-layout/seller-layout.component';
import { SellerDashboardComponent } from './seller-dashboard/seller-dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: SellerLayoutComponent,
    children: [
      {
        path: 'dashboard',
        component: SellerDashboardComponent,
      },
      {
        path: 'products',
        loadComponent: () =>
          import('./seller-products/seller-products.component').then((m) => m.SellerProductsComponent),
      },
      {
        path: 'orders',
        loadComponent: () =>
          import('./seller-orders/seller-orders.component').then((m) => m.SellerOrdersComponent),
      },
      {
        path: 'analytics',
        loadComponent: () =>
          import('./seller-analytics/seller-analytics.component').then((m) => m.SellerAnalyticsComponent),
      },
      {
        path: 'settings',
        loadComponent: () =>
          import('./seller-settings/seller-settings.component').then((m) => m.SellerSettingsComponent),
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full',
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class SellerRoutingModule {}
