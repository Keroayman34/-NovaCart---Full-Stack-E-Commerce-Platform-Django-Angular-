import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { AdminLayoutComponent } from "./admin-layout/admin-layout.component";
import { AdminGuard } from "../../core/guards/admin.guard";

const routes: Routes = [
  {
    path: "",
    component: AdminLayoutComponent,
    canActivate: [AdminGuard],
    children: [
      {
        path: "dashboard",
        loadComponent: () =>
          import("./dashboard/dashboard.component").then(
            (m) => m.AdminDashboardComponent,
          ),
      },
      {
        path: "users",
        loadComponent: () =>
          import("./users/users.component").then((m) => m.AdminUsersComponent),
      },
      {
        path: "products",
        loadComponent: () =>
          import("./products/products.component").then(
            (m) => m.AdminProductsComponent,
          ),
      },
      {
        path: "orders",
        loadComponent: () =>
          import("./orders/orders.component").then(
            (m) => m.AdminOrdersComponent,
          ),
      },
      {
        path: "categories",
        loadComponent: () =>
          import("./categories/categories.component").then(
            (m) => m.AdminCategoriesComponent,
          ),
      },
      {
        path: "",
        redirectTo: "dashboard",
        pathMatch: "full",
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AdminRoutingModule {}
