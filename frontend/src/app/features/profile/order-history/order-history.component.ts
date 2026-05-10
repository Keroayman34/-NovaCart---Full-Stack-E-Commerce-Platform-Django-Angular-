import { Component, OnInit } from "@angular/core";
import { ProfileService } from "../../../core/services/profile.service";
import { Order } from "../../../shared/models/order.model";

@Component({
  selector: "app-order-history",
  templateUrl: "./order-history.component.html",
  styleUrls: ["./order-history.component.scss"],
})
export class OrderHistoryComponent implements OnInit {
  orders: Order[] = [];
  isLoading = true;
  errorMessage = "";

  constructor(private profileService: ProfileService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  // display order list
  loadOrders(): void {
    this.isLoading = true;
    this.errorMessage = "";

    this.profileService.getOrders().subscribe({
      next: (orders) => {
        this.orders = orders;
      },
      error: () => {
        this.errorMessage = "Unable to load orders.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }
}
