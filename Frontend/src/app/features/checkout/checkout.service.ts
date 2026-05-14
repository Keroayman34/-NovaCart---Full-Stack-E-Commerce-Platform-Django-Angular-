import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

export type PaymentMethod = "card" | "paypal" | "cash" | "wallet";

export interface CardDetails {
  cardNumber: string;
  expiry: string;
  cvv: string;
}

export interface Order {
  id: number;
  orderNumber: string;
  userId: number;
  totalPrice: number;
  status: string;
  shippingAddress?: string;
  createdAt: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id: number;
  productId: number;
  productName: string;
  quantity: number;
  price: number;
}

@Injectable({
  providedIn: "root",
})
export class CheckoutService {
  private readonly paymentMethodSubject = new BehaviorSubject<PaymentMethod>("card");
  private readonly cardDetailsSubject = new BehaviorSubject<CardDetails | null>(null);
  private readonly orderSubject = new BehaviorSubject<Order | null>(null);

  readonly paymentMethod$ = this.paymentMethodSubject.asObservable();
  readonly cardDetails$ = this.cardDetailsSubject.asObservable();
  readonly order$ = this.orderSubject.asObservable();

  setPaymentMethod(method: PaymentMethod): void {
    this.paymentMethodSubject.next(method);
  }

  getPaymentMethod(): PaymentMethod {
    return this.paymentMethodSubject.value;
  }

  setCardDetails(details: CardDetails): void {
    this.cardDetailsSubject.next(details);
  }

  clearCardDetails(): void {
    this.cardDetailsSubject.next(null);
  }

  setOrder(order: Order): void {
    this.orderSubject.next(order);
  }

  getOrder(): Order | null {
    return this.orderSubject.value;
  }

  getPaymentPayload(): { method: PaymentMethod; card?: CardDetails } {
    const method = this.getPaymentMethod();
    const card = this.cardDetailsSubject.value;

    if (method === "card" && card) {
      return { method, card };
    }

    return { method };
  }

  clearCheckout(): void {
    this.paymentMethodSubject.next("card");
    this.cardDetailsSubject.next(null);
    this.orderSubject.next(null);
  }
}
