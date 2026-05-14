import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Router } from "@angular/router";
import { environment } from "../../../../environments/environment";
import { AuthService } from "../../core/services/auth.service";
import { CheckoutService } from "./checkout.service";
import { ShippingFormComponent } from "./shipping-form/shipping-form.component";
import { PaymentMethodComponent } from "./payment-method/payment-method.component";
import { OrderSummaryComponent } from "./order-summary/order-summary.component";
import { GuestCheckoutComponent } from "./guest-checkout/guest-checkout.component";

interface OrderPayload {
  items: OrderItem[];
  shippingAddress: string;
  totalPrice: number;
  status: string;
  guestEmail?: string;
}

interface OrderItem {
  productId: number;
  quantity: number;
  price: number;
}

interface PaymentPayload {
  orderId: number;
  method: string;
  card?: any;
}

interface GuestCheckoutData {
  email: string;
  name: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  postalCode: string;
}

@Component({
  selector: "app-checkout",
  standalone: true,
  imports: [
    CommonModule,
    ShippingFormComponent,
    PaymentMethodComponent,
    OrderSummaryComponent,
    GuestCheckoutComponent,
  ],
  templateUrl: "./checkout.component.html",
  styleUrls: ["./checkout.component.scss"],
})
export class CheckoutComponent implements OnInit {
  isProcessing = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;
  isLoggedIn = false;
  guestData: GuestCheckoutData | null = null;

  private apiUrl = environment.apiUrl || "";

  constructor(
    private http: HttpClient,
    private checkoutService: CheckoutService,
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();

    // Check for existing guest data in localStorage
    const savedGuestData = localStorage.getItem("guest_checkout_data");
    if (savedGuestData) {
      try {
        this.guestData = JSON.parse(savedGuestData);
      } catch (e) {
        this.guestData = null;
      }
    }
  }

  onGuestDataSubmitted(data: GuestCheckoutData): void {
    this.guestData = data;
  }

  onLoginRequested(): void {
    this.router.navigate(["/login"], {
      queryParams: { returnUrl: "/checkout" },
    });
  }

  onSubmit(): void {
    if (this.isProcessing) return;

    this.errorMessage = null;
    this.successMessage = null;

    // For logged-in users, validate form components exist
    if (this.isLoggedIn) {
      const shippingForm = document.querySelector("app-shipping-form");
      const paymentForm = document.querySelector("app-payment-method");

      if (!shippingForm || !paymentForm) {
        this.errorMessage = "Form components not initialized";
        return;
      }
    }

    // For guest checkout, validate guest data
    if (!this.isLoggedIn && !this.guestData) {
      this.errorMessage = "Please complete guest checkout form";
      return;
    }

    // Get cart items from localStorage
    const cartItemsRaw = localStorage.getItem("cart_items");
    let cartItems: OrderItem[] = [];

    if (cartItemsRaw) {
      try {
        const parsed = JSON.parse(cartItemsRaw);
        cartItems = Array.isArray(parsed) ? parsed : [];
      } catch (e) {
        cartItems = [];
      }
    }

    if (cartItems.length === 0) {
      this.errorMessage = "Your cart is empty";
      return;
    }

    // Calculate total from cart items
    const totalPrice = cartItems.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0,
    );

    // Prepare shipping address based on user type
    const shippingAddress = this.isLoggedIn
      ? this.getShippingAddressFromForm()
      : this.getGuestShippingAddress();

    if (!shippingAddress) {
      this.errorMessage = "Please fill in all shipping details";
      return;
    }

    this.isProcessing = true;

    // Step 1: Create order
    const orderPayload: OrderPayload = {
      items: cartItems,
      shippingAddress,
      totalPrice,
      status: "pending",
      guestEmail: !this.isLoggedIn ? this.guestData?.email : undefined,
    };

    this.http
      .post<{ id: number; orderNumber: string }>(`${this.apiUrl}/orders/`, orderPayload)
      .subscribe({
        next: (orderResponse) => {
          // Step 2: Process payment
          const paymentPayload: PaymentPayload = {
            orderId: orderResponse.id,
            ...this.checkoutService.getPaymentPayload(),
          };

          this.http
            .post<{ status: string }>(`${this.apiUrl}/payments/`, paymentPayload)
            .subscribe({
              next: () => {
                // Success: clear cart and navigate to confirmation
                localStorage.removeItem("cart_items");
                localStorage.removeItem("guest_checkout_data");
                this.checkoutService.clearCheckout();
                this.successMessage = "Order placed successfully!";

                // Navigate to order confirmation page
                setTimeout(() => {
                  this.router.navigate(["/order-confirmation", orderResponse.id]);
                }, 500);
              },
              error: (error) => {
                console.error("Payment failed:", error);
                this.errorMessage =
                  error.error?.message ||
                  "Payment processing failed. Please try again.";
                this.isProcessing = false;
              },
            });
        },
        error: (error) => {
          console.error("Order creation failed:", error);
          this.errorMessage =
            error.error?.message ||
            "Failed to create order. Please try again.";
          this.isProcessing = false;
        },
      });
  }

  private getShippingAddressFromForm(): string | null {
    // Try to extract shipping form data from the DOM or component
    // For now, we'll construct it from localStorage as fallback
    const saved = this.getSavedAddress();

    if (saved.address && saved.city && saved.country && saved.postalCode) {
      return `${saved.address}, ${saved.city}, ${saved.country} ${saved.postalCode}`;
    }

    return null;
  }

  private getGuestShippingAddress(): string | null {
    if (!this.guestData) return null;

    const { address, city, country, postalCode } = this.guestData;

    if (address && city && country && postalCode) {
      return `${address}, ${city}, ${country} ${postalCode}`;
    }

    return null;
  }

  private getSavedAddress(): any {
    const profileRaw = localStorage.getItem("user_profile");
    const shippingRaw = localStorage.getItem("saved_shipping_address");

    let profile: any = {};
    let shipping: any = {};

    try {
      profile = profileRaw ? JSON.parse(profileRaw) : {};
    } catch {
      profile = {};
    }

    try {
      shipping = shippingRaw ? JSON.parse(shippingRaw) : {};
    } catch {
      shipping = {};
    }

    return {
      name: shipping.name || profile.name || profile.fullName || "",
      phone: shipping.phone || profile.phone || "",
      address: shipping.address || profile.address || "",
      city: shipping.city || profile.city || "",
      country: shipping.country || profile.country || "",
      postalCode:
        shipping.postalCode || shipping.postal_code || profile.postalCode || profile.postal_code || "",
    };
  }
}
