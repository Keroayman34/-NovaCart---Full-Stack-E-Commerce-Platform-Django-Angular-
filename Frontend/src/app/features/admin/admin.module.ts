import { NgModule } from "@angular/core";
import { AdminRoutingModule } from "./admin-routing.module";
import { AdminLayoutComponent } from "./admin-layout/admin-layout.component";

@NgModule({
  imports: [AdminRoutingModule, AdminLayoutComponent],
})
export class AdminModule {}
