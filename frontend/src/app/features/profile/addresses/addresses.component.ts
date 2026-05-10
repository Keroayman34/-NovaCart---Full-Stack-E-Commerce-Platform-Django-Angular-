import { Component, OnInit } from "@angular/core";
import { ProfileService } from "../../../core/services/profile.service";
import { Address } from "../../../shared/models/user.model";

@Component({
  selector: "app-addresses",
  templateUrl: "./addresses.component.html",
  styleUrls: ["./addresses.component.scss"],
})
export class AddressesComponent implements OnInit {
  addresses: Address[] = [];
  selectedAddress: Address | null = null;
  isFormVisible = false;
  isLoading = true;
  errorMessage = "";

  constructor(private profileService: ProfileService) {}

  ngOnInit(): void {
    this.loadAddresses();
  }

  // load user addresses
  loadAddresses(): void {
    this.isLoading = true;
    this.errorMessage = "";

    this.profileService.getAddresses().subscribe({
      next: (addresses) => {
        this.addresses = addresses;
      },
      error: () => {
        this.errorMessage = "Unable to load addresses.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  // open add address form
  onAddAddress(): void {
    this.selectedAddress = null;
    this.isFormVisible = true;
  }

  // edit selected address
  onEditAddress(address: Address): void {
    this.selectedAddress = { ...address };
    this.isFormVisible = true;
  }

  // save address changes
  onSaveAddress(address: Address): void {
    if (this.selectedAddress?.id) {
      const addressId = this.selectedAddress.id;
      this.profileService.updateAddress(addressId, address).subscribe({
        next: (updated) => {
          this.addresses = this.addresses.map((item) =>
            item.id === addressId ? updated : item,
          );
          this.isFormVisible = false;
        },
        error: () => {
          this.errorMessage = "Unable to update address.";
        },
      });
      return;
    }

    this.profileService.addAddress(address).subscribe({
      next: (created) => {
        this.addresses = [...this.addresses, created];
        this.isFormVisible = false;
      },
      error: () => {
        this.errorMessage = "Unable to add address.";
      },
    });
  }

  // cancel form
  onCancelAddress(): void {
    this.isFormVisible = false;
  }

  // delete address
  onDeleteAddress(addressId?: number): void {
    if (!addressId) {
      return;
    }

    this.profileService.deleteAddress(addressId).subscribe({
      next: () => {
        this.addresses = this.addresses.filter((item) => item.id !== addressId);
      },
      error: () => {
        this.errorMessage = "Unable to delete address.";
      },
    });
  }
}
