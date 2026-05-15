import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-seller-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
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

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.loadUserProfile();
  }

  loadUserProfile(): void {
    // In a real app, you would fetch user profile from a service
    // For now, we'll use placeholder data that could be fetched from AuthService
    const user = this.authService.getCurrentUser?.();
    if (user) {
      this.userProfile = {
        name: user.name || 'Seller',
        email: user.email,
        avatar: user.avatar,
      };
    } else {
      this.userProfile = {
        name: 'Seller',
        email: 'seller@example.com',
      };
    }
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }

  closeSidebar(): void {
    this.sidebarOpen = false;
  }

  logout(): void {
    if (confirm('Are you sure you want to logout?')) {
      this.authService.logout();
      this.router.navigate(['/login']);
    }
  }
}
