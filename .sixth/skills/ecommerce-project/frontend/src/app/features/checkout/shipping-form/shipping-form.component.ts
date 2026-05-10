import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";

import { AuthService } from "../../../core/services/auth.service";

interface SavedAddress {
  name?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  postalCode?: string;
}

@Component({
  selector: "app-shipping-form",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: "./shipping-form.component.html",
  styleUrls: ["./shipping-form.component.scss"],
})
export class ShippingFormComponent implements OnInit {
  readonly shippingForm = this.fb.group({
    name: ["", [Validators.required]],
    phone: ["", [Validators.required, Validators.pattern(/^\+?[0-9\s\-()]{7,20}$/)]],
    address: ["", [Validators.required]],
    city: ["", [Validators.required]],
    country: ["", [Validators.required]],
    postalCode: ["", [Validators.required, Validators.minLength(3)]],
  });

  isLoggedIn = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
  ) {}

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();

    if (this.isLoggedIn) {
      this.prefillFromProfile();
    }
  }

  useSavedAddress(): void {
    const saved = this.getSavedAddress();
    this.shippingForm.patchValue({
      name: saved.name || "",
      phone: saved.phone || "",
      address: saved.address || "",
      city: saved.city || "",
      country: saved.country || "",
      postalCode: saved.postalCode || "",
    });
  }

  private prefillFromProfile(): void {
    const saved = this.getSavedAddress();

    this.shippingForm.patchValue({
      name: saved.name || "",
      phone: saved.phone || "",
      address: saved.address || "",
      city: saved.city || "",
      country: saved.country || "",
      postalCode: saved.postalCode || "",
    });
  }

  private getSavedAddress(): SavedAddress {
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
      postalCode: shipping.postalCode || shipping.postal_code || profile.postalCode || profile.postal_code || "",
    };
  }

  controlInvalid(controlName: string): boolean {
    const control = this.shippingForm.get(controlName);
    return !!control && control.invalid && (control.dirty || control.touched);
  }
}
