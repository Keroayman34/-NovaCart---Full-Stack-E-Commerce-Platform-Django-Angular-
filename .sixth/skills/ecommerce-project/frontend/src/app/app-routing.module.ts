import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ProductListComponent } from "./features/products/product-list/product-list.component";
import { ProfilePageComponent } from "./features/profile/profile-page/profile-page.component";
import { CheckoutComponent } from "./features/checkout/checkout.component";
import { OrderConfirmationComponent } from "./features/checkout/order-confirmation/order-confirmation.component";
import { AuthGuard } from "./core/guards/auth.guard";
import { AdminGuard } from "./core/guards/admin.guard";

const routes: Routes = [
  { path: "", redirectTo: "products", pathMatch: "full" },
  { path: "products", component: ProductListComponent },
  { path: "checkout", component: CheckoutComponent },
  { path: "order-confirmation/:id", component: OrderConfirmationComponent },
  {
    path: "profile",
    component: ProfilePageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "admin",
    loadChildren: () =>
      import("./features/admin/admin.module").then((m) => m.AdminModule),
    canActivate: [AdminGuard],
  },
  { path: "**", redirectTo: "products" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
