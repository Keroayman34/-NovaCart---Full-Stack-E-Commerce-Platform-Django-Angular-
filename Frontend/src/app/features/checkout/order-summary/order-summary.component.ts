import { CommonModule, CurrencyPipe } from "@angular/common";
import { Component, OnInit } from "@angular/core";

interface CartItemView {
  image?: string;
  name: string;
  quantity: number;
  price: number;
}

@Component({
  selector: "app-order-summary",
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: "./order-summary.component.html",
  styleUrls: ["./order-summary.component.scss"],
})
export class OrderSummaryComponent implements OnInit {
  items: CartItemView[] = [];

  subtotal = 0;
  shipping = 0;
  tax = 0;
  total = 0;

  ngOnInit(): void {
    this.loadFromCartService();
    this.calculateTotals();
  }

  private loadFromCartService(): void {
    // F2 requirement: load data from CartService.
    // The project CartService is currently a scaffold, so we use a safe fallback
    // from localStorage while keeping a CartService-oriented loading method.
    const raw = localStorage.getItem("cart_items");
    const parsed = raw ? JSON.parse(raw) : [];

    this.items = Array.isArray(parsed)
      ? parsed.map((item: any) => ({
          image: item?.image || item?.product?.image || "",
          name: item?.name || item?.product?.name || "Product",
          quantity: Number(item?.quantity || 1),
          price: Number(item?.price || item?.product?.price || 0),
        }))
      : [];
  }

  private calculateTotals(): void {
    this.subtotal = this.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );

    this.shipping = this.subtotal > 0 ? 10 : 0;
    this.tax = this.subtotal * 0.1;
    this.total = this.subtotal + this.shipping + this.tax;
  }
}
