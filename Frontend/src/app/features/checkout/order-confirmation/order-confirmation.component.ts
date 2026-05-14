import { CommonModule, CurrencyPipe } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";
import { environment } from "../../../../../environments/environment";
import { Order } from "../checkout.service";

@Component({
  selector: "app-order-confirmation",
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: "./order-confirmation.component.html",
  styleUrls: ["./order-confirmation.component.scss"],
})
export class OrderConfirmationComponent implements OnInit {
  order: Order | null = null;
  isLoading = true;
  errorMessage: string | null = null;

  private apiUrl = environment.apiUrl || "";

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      const orderId = params["id"];
      if (orderId) {
        this.loadOrder(orderId);
      }
    });
  }

  private loadOrder(orderId: number): void {
    this.isLoading = true;
    this.errorMessage = null;

    this.http.get<Order>(`${this.apiUrl}/orders/${orderId}/`).subscribe({
      next: (order) => {
        this.order = order;
        this.isLoading = false;
      },
      error: (error) => {
        console.error("Failed to load order:", error);
        this.errorMessage = "Failed to load order details. Please try again.";
        this.isLoading = false;
      },
    });
  }

  continueShopping(): void {
    // Clear cart from localStorage
    localStorage.removeItem("cart_items");
    this.router.navigate(["/products"]);
  }

  getFormattedDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }
}
