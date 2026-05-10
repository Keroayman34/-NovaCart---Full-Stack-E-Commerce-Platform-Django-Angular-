import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { AdminUsersService, User } from "./users.service";

@Component({
  selector: "app-admin-users",
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: "./users.component.html",
  styleUrls: ["./users.component.scss"],
})
export class AdminUsersComponent implements OnInit {
  users: User[] = [];
  isLoading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  // Filters
  selectedRole: string = "";
  selectedStatus: string = "";
  roleOptions = ["admin", "seller", "customer"];
  statusOptions = [
    { label: "Active", value: "active" },
    { label: "Restricted", value: "restricted" },
  ];

  // Pagination
  currentPage = 1;
  totalCount = 0;
  pageSize = 10;

  constructor(private usersService: AdminUsersService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.isLoading = true;
    this.errorMessage = null;

    this.usersService
      .getUsers(this.currentPage, this.selectedRole || undefined, this.selectedStatus || undefined)
      .subscribe({
        next: (response) => {
          this.users = response.results;
          this.totalCount = response.count;
          this.isLoading = false;
        },
        error: (error) => {
          console.error("Failed to load users:", error);
          this.errorMessage = "Failed to load users. Please try again.";
          this.isLoading = false;
        },
      });
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadUsers();
  }

  restrictUser(user: User): void {
    if (!confirm(`Restrict user ${user.name}? They will no longer be able to access the platform.`)) {
      return;
    }

    this.usersService.restrictUser(user.id).subscribe({
      next: () => {
        this.successMessage = `User ${user.name} has been restricted.`;
        this.loadUsers();
        setTimeout(() => {
          this.successMessage = null;
        }, 3000);
      },
      error: (error) => {
        console.error("Failed to restrict user:", error);
        this.errorMessage = `Failed to restrict ${user.name}. Please try again.`;
      },
    });
  }

  activateUser(user: User): void {
    if (!confirm(`Activate user ${user.name}?`)) {
      return;
    }

    this.usersService.activateUser(user.id).subscribe({
      next: () => {
        this.successMessage = `User ${user.name} has been activated.`;
        this.loadUsers();
        setTimeout(() => {
          this.successMessage = null;
        }, 3000);
      },
      error: (error) => {
        console.error("Failed to activate user:", error);
        this.errorMessage = `Failed to activate ${user.name}. Please try again.`;
      },
    });
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.getTotalPages()) return;
    this.currentPage = page;
    this.loadUsers();
  }

  getTotalPages(): number {
    return Math.ceil(this.totalCount / this.pageSize);
  }

  getPageNumbers(): number[] {
    const total = this.getTotalPages();
    const pages: number[] = [];
    const maxPagesToShow = 5;

    let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(total, startPage + maxPagesToShow - 1);

    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  }

  getStatusBadgeClass(isActive: boolean): string {
    return isActive ? "status-active" : "status-restricted";
  }

  getStatusLabel(isActive: boolean): string {
    return isActive ? "Active" : "Restricted";
  }
}
