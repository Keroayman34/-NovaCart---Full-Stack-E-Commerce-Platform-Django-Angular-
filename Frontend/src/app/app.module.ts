import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { AuthModule } from "./features/auth/auth.module";
import { ProductsModule } from "./features/products/products.module";
import { ProfileModule } from "./features/profile/profile.module";
import { AdminModule } from "./features/admin/admin.module";
import { NavbarComponent } from "./shared/components/navbar/navbar.component";
import { FooterComponent } from "./shared/components/footer/footer.component";

@NgModule({
  declarations: [AppComponent, NavbarComponent, FooterComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    AuthModule,
    ProductsModule,
    ProfileModule,
    AdminModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
