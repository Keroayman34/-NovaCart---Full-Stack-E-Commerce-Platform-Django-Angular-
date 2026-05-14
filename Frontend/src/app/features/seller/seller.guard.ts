import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class SellerGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    const isLoggedIn = this.authService.isLoggedIn();
    const userRole = this.authService.getRole();

    if (!isLoggedIn) {
      this.router.navigate(['/login']);
      return false;
    }

    if (userRole !== 'seller') {
      this.router.navigate(['/products']);
      return false;
    }

    return true;
  }
}
