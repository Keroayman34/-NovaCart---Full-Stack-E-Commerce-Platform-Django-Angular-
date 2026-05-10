import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivate, Router } from "@angular/router";
import { AuthService } from "../services/auth.service";

@Injectable({
  providedIn: "root",
})
export class RoleGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  // allow access only for matching roles
  canActivate(route: ActivatedRouteSnapshot): boolean {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(["/login"]);
      return false;
    }

    const allowedRoles = route.data["roles"] as string[] | undefined;
    const userRole = this.authService.getRole();

    if (!allowedRoles || !userRole) {
      return false;
    }

    if (allowedRoles.includes(userRole)) {
      return true;
    }

    this.router.navigate(["/products"]);
    return false;
  }
}
