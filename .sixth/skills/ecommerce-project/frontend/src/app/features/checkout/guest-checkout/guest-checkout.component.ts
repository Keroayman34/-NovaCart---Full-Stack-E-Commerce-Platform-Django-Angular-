import { CommonModule } from "@angular/common";
import { Component, EventEmitter, OnInit, Output } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { Router } from "@angular/router";

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
  selector: "app-guest-checkout",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: "./guest-checkout.component.html",
  styleUrls: ["./guest-checkout.component.scss"],
})
export class GuestCheckoutComponent implements OnInit {
  @Output() guestDataSubmitted = new EventEmitter<GuestCheckoutData>();
  @Output() loginRequested = new EventEmitter<void>();

  isGuestMode = false;

  readonly guestForm = this.fb.group({
    email: ["", [Validators.required, Validators.email]],
    name: ["", [Validators.required]],
    phone: ["", [Validators.required, Validators.pattern(/^\+?[0-9\s\-()]{7,20}$/)]],
    address: ["", [Validators.required]],
    city: ["", [Validators.required]],
    country: ["", [Validators.required]],
    postalCode: ["", [Validators.required, Validators.minLength(3)]],
  });

  constructor(
    private fb: FormBuilder,
    private router: Router,
  ) {}

  ngOnInit(): void {
    // Component initialization
  }

  continueAsGuest(): void {
    this.isGuestMode = true;
  }

  goToLogin(): void {
    this.loginRequested.emit();
  }

  submitGuestForm(): void {
    if (this.guestForm.invalid) {
      this.markFormGroupTouched(this.guestForm);
      return;
    }

    const guestData: GuestCheckoutData = {
      email: this.guestForm.get("email")?.value || "",
      name: this.guestForm.get("name")?.value || "",
      phone: this.guestForm.get("phone")?.value || "",
      address: this.guestForm.get("address")?.value || "",
      city: this.guestForm.get("city")?.value || "",
      country: this.guestForm.get("country")?.value || "",
      postalCode: this.guestForm.get("postalCode")?.value || "",
    };

    // Save guest data to localStorage for order submission
    localStorage.setItem("guest_checkout_data", JSON.stringify(guestData));

    // Emit event to parent component
    this.guestDataSubmitted.emit(guestData);
  }

  backToChoice(): void {
    this.isGuestMode = false;
    this.guestForm.reset();
  }

  controlInvalid(controlName: string): boolean {
    const control = this.guestForm.get(controlName);
    return !!control && control.invalid && (control.dirty || control.touched);
  }

  private markFormGroupTouched(formGroup: any): void {
    Object.keys(formGroup.controls).forEach((key) => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }
}
