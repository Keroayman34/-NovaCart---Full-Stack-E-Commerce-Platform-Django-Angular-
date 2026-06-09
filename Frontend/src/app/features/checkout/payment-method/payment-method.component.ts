import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";

import { CheckoutService, PaymentMethod } from "../checkout.service";

@Component({
  selector: "app-payment-method",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: "./payment-method.component.html",
  styleUrls: ["./payment-method.component.scss"],
})
export class PaymentMethodComponent {
  readonly methods: { value: PaymentMethod; label: string }[] = [
    { value: "card", label: "Credit Card" },
    { value: "paypal", label: "PayPal" },
    { value: "cash", label: "Cash on Delivery" },
    { value: "wallet", label: "Wallet" },
  ];

  readonly paymentForm = this.fb.group({
    method: this.fb.nonNullable.control<PaymentMethod>("card"),
    cardNumber: ["", [Validators.required, Validators.pattern(/^[0-9]{12,19}$/)]],
    expiry: ["", [Validators.required, Validators.pattern(/^(0[1-9]|1[0-2])\/[0-9]{2}$/)]],
    cvv: ["", [Validators.required, Validators.pattern(/^[0-9]{3,4}$/)]],
  });

  constructor(
    private fb: FormBuilder,
    private checkoutService: CheckoutService,
  ) {
    this.paymentForm.controls.method.valueChanges.subscribe((method) => {
      this.checkoutService.setPaymentMethod(method);
      this.applyCardValidation(method);
    });

    this.paymentForm.valueChanges.subscribe(() => {
      this.syncServiceState();
    });

    this.applyCardValidation(this.paymentForm.controls.method.value);
    this.syncServiceState();
  }

  get selectedMethod(): PaymentMethod {
    return this.paymentForm.controls.method.value;
  }

  get showCardForm(): boolean {
    return this.selectedMethod === "card";
  }

  controlInvalid(name: "cardNumber" | "expiry" | "cvv"): boolean {
    const control = this.paymentForm.get(name);
    return !!control && control.invalid && (control.dirty || control.touched);
  }

  private applyCardValidation(method: PaymentMethod): void {
    const cardControls = [
      this.paymentForm.controls.cardNumber,
      this.paymentForm.controls.expiry,
      this.paymentForm.controls.cvv,
    ];

    if (method === "card") {
      cardControls.forEach((control) => control.enable({ emitEvent: false }));
    } else {
      cardControls.forEach((control) => {
        control.disable({ emitEvent: false });
        control.reset("", { emitEvent: false });
      });
    }
  }

  private syncServiceState(): void {
    this.checkoutService.setPaymentMethod(this.selectedMethod);

    if (this.selectedMethod === "card") {
      this.checkoutService.setCardDetails({
        cardNumber: this.paymentForm.controls.cardNumber.value || "",
        expiry: this.paymentForm.controls.expiry.value || "",
        cvv: this.paymentForm.controls.cvv.value || "",
      });
    } else {
      this.checkoutService.clearCardDetails();
    }
  }
}
