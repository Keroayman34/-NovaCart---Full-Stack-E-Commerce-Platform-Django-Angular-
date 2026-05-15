import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ProductListComponent } from "./features/products/product-list/product-list.component";
import { ProductDetailComponent } from "./features/products/product-detail/product-detail.component";
import { ProfilePageComponent } from "./features/profile/profile-page/profile-page.component";
import { AddressesComponent } from "./features/profile/addresses/addresses.component";
import { WishlistComponent } from "./features/profile/wishlist/wishlist.component";
import { OrderHistoryComponent } from "./features/profile/order-history/order-history.component";
import { OrderDetailComponent } from "./features/profile/order-history/order-detail/order-detail.component";
import { CheckoutComponent } from "./features/checkout/checkout.component";
import { OrderConfirmationComponent } from "./features/checkout/order-confirmation/order-confirmation.component";
import { AuthGuard } from "./core/guards/auth.guard";
import { AdminGuard } from "./core/guards/admin.guard";
import { SellerGuard } from "./features/seller/seller.guard";

const routes: Routes = [
  { path: "", redirectTo: "products", pathMatch: "full" },
  { path: "products", component: ProductListComponent },
  { path: "products/:id", component: ProductDetailComponent },
  { path: "checkout", component: CheckoutComponent },
  { path: "order-confirmation/:id", component: OrderConfirmationComponent },
  {
    path: "profile",
    component: ProfilePageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "profile/addresses",
    component: AddressesComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "profile/wishlist",
    component: WishlistComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "profile/orders",
    component: OrderHistoryComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "profile/orders/:id",
    component: OrderDetailComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "admin",
    loadChildren: () =>
      import("./features/admin/admin.module").then((m) => m.AdminModule),
    canActivate: [AdminGuard],
  },
  {
    path: "seller",
    loadChildren: () =>
      import("./features/seller/seller.module").then((m) => m.SellerModule),
    canActivate: [SellerGuard],
  },
  { path: "**", redirectTo: "products" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
