import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { SellerProfileService } from '../../../core/services/seller-profile.service';

@Component({
  selector: 'app-seller-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './seller-layout.component.html',
  styleUrls: ['./seller-layout.component.scss'],
})
export class SellerLayoutComponent implements OnInit {
  sidebarOpen = false;
  userProfile: { name?: string; email?: string; avatar?: string } = {};

  navItems = [
    { label: 'Dashboard', route: '/seller/dashboard', icon: '📊' },
    { label: 'My Products', route: '/seller/products', icon: '📦' },
    { label: 'My Orders', route: '/seller/orders', icon: '📋' },
    { label: 'Analytics', route: '/seller/analytics', icon: '📈' },
    { label: 'Settings', route: '/seller/settings', icon: '⚙️' },
  ];

  constructor(
    private authService: AuthService,
    private sellerProfileService: SellerProfileService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.loadSellerProfile();
  }

  loadSellerProfile(): void {
    if (!this.authService.isLoggedIn()) return;
    this.sellerProfileService.getProfile().subscribe({
      next: (profile) => {
        const email = profile.user?.email || '';
        this.userProfile = {
          name: profile.shop_name || email,
          email: email,
          avatar: profile.shop_logo || undefined,
        };
      },
      error: () => {
        this.authService.getCurrentUser().subscribe({
          next: (user) => {
            this.userProfile = {
              name: user.email || 'Seller',
              email: user.email,
              avatar: user.avatar,
            };
          },
          error: () => {
            this.userProfile = { name: 'Seller', email: 'seller@example.com' };
          },
        });
      },
    });
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }

  closeSidebar(): void {
    this.sidebarOpen = false;
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
