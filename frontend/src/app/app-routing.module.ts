import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ProductListComponent } from "./features/products/product-list/product-list.component";
import { ProductDetailComponent } from "./features/products/product-detail/product-detail.component";
import { ProfilePageComponent } from "./features/profile/profile-page/profile-page.component";
import { AddressesComponent } from "./features/profile/addresses/addresses.component";
import { WishlistComponent } from "./features/profile/wishlist/wishlist.component";
import { OrderHistoryComponent } from "./features/profile/order-history/order-history.component";
import { OrderDetailComponent } from "./features/profile/order-history/order-detail/order-detail.component";
import { AdminDashboardComponent } from "./features/admin/dashboard/dashboard.component";
import { AuthGuard } from "./core/guards/auth.guard";
import { RoleGuard } from "./core/guards/role.guard";

const routes: Routes = [
  { path: "", redirectTo: "products", pathMatch: "full" },
  { path: "products", component: ProductListComponent },
  { path: "products/:id", component: ProductDetailComponent },
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
    component: AdminDashboardComponent,
    canActivate: [RoleGuard],
    data: { roles: ["admin"] },
  },
  { path: "**", redirectTo: "products" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
