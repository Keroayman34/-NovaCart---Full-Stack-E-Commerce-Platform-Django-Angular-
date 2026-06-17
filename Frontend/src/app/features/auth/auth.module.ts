import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ReactiveFormsModule } from "@angular/forms";

import { AuthRoutingModule } from "./auth-routing.module";
import { LoginComponent } from "./login/login.component";
import { RegisterComponent } from "./register/register.component";
import { VerifyEmailComponent } from "./verify-email/verify-email.component";

@NgModule({
  declarations: [LoginComponent, RegisterComponent, VerifyEmailComponent],
  imports: [CommonModule, ReactiveFormsModule, AuthRoutingModule],
})
export class AuthModule {}
