import { Injectable } from "@angular/core";
import { CanActivate, ActivatedRouteSnapshot, Router } from "@angular/router";
import { AuthService } from "../services/auth.service";

@Injectable({
  providedIn: "root",
})
export class AdminGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  canActivate(route?: ActivatedRouteSnapshot): boolean {
    // Check if user is logged in
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(["/login"]);
      return false;
    }

    // Check if user has admin role
    const userRole = this.authService.getRole();

    if (userRole === "admin") {
      return true;
    }

    // Redirect unauthorized users to home
    this.router.navigate(["/products"]);
    return false;
  }
}
