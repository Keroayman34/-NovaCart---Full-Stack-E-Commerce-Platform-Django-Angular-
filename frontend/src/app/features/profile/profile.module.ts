import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ReactiveFormsModule } from "@angular/forms";
import { RouterModule } from "@angular/router";
import { ProfilePageComponent } from "./profile-page/profile-page.component";
import { AddressesComponent } from "./addresses/addresses.component";
import { AddressFormComponent } from "./addresses/address-form/address-form.component";
import { WishlistComponent } from "./wishlist/wishlist.component";
import { OrderHistoryComponent } from "./order-history/order-history.component";
import { OrderDetailComponent } from "./order-history/order-detail/order-detail.component";

@NgModule({
  declarations: [
    ProfilePageComponent,
    AddressesComponent,
    AddressFormComponent,
    WishlistComponent,
    OrderHistoryComponent,
    OrderDetailComponent,
  ],
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  exports: [
    ProfilePageComponent,
    AddressesComponent,
    WishlistComponent,
    OrderHistoryComponent,
    OrderDetailComponent,
  ],
})
export class ProfileModule {}
