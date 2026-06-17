import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { ProfileService } from "../../../../core/services/profile.service";
import { Order } from "../../../../shared/models/order.model";

@Component({
  selector: "app-order-detail",
  templateUrl: "./order-detail.component.html",
  styleUrls: ["./order-detail.component.scss"],
})
export class OrderDetailComponent implements OnInit {
  order: Order | null = null;
  isLoading = true;
  errorMessage = "";

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private profileService: ProfileService,
  ) {}

  ngOnInit(): void {
    this.loadOrder();
  }

  loadOrder(): void {
    const orderId = Number(this.route.snapshot.paramMap.get("id"));

    if (!orderId) {
      this.router.navigate(["/profile/orders"]);
      return;
    }

    this.isLoading = true;
    this.errorMessage = "";

    this.profileService.getOrder(orderId).subscribe({
      next: (order) => {
        this.order = order;
      },
      error: () => {
        this.errorMessage = "Unable to load order details.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }
}
