import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ProductListComponent } from "./features/products/product-list/product-list.component";
import { ProfilePageComponent } from "./features/profile/profile-page/profile-page.component";
import { AdminDashboardComponent } from "./features/admin/dashboard/dashboard.component";
import { AuthGuard } from "./core/guards/auth.guard";
import { RoleGuard } from "./core/guards/role.guard";

const routes: Routes = [
  { path: "", redirectTo: "products", pathMatch: "full" },
  { path: "products", component: ProductListComponent },
  {
    path: "profile",
    component: ProfilePageComponent,
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
