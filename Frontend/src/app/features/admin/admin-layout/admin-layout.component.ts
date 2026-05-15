import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { RouterModule, Router } from "@angular/router";
import { AuthService } from "../../../core/services/auth.service";

interface NavItem {
  label: string;
  route: string;
  icon: string;
}

@Component({
  selector: "app-admin-layout",
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: "./admin-layout.component.html",
  styleUrls: ["./admin-layout.component.scss"],
})
export class AdminLayoutComponent implements OnInit {
  isSidebarOpen = true;
  userName: string | null = null;

  navItems: NavItem[] = [
    { label: "Dashboard", route: "dashboard", icon: "📊" },
    { label: "Users", route: "users", icon: "👥" },
    { label: "Products", route: "products", icon: "📦" },
    { label: "Orders", route: "orders", icon: "📋" },
    { label: "Categories", route: "categories", icon: "🏷️" },
  ];

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    // Get user name from localStorage or profile
    const profileRaw = localStorage.getItem("user_profile");
    if (profileRaw) {
      try {
        const profile = JSON.parse(profileRaw);
        this.userName = profile.name || profile.fullName || "Admin";
      } catch (e) {
        this.userName = "Admin";
      }
    }
  }

  toggleSidebar(): void {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  isActive(route: string): boolean {
    return this.router.url.includes(`/admin/${route}`);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(["/login"]);
  }
}
