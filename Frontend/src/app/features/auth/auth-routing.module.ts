import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { LoginComponent } from "./login/login.component";
import { RegisterComponent } from "./register/register.component";
import { VerifyEmailComponent } from "./verify-email/verify-email.component";

const routes: Routes = [
  { path: "/auth/login", component: LoginComponent },
  { path: "/auth/register", component: RegisterComponent },
  { path: "verify-email", component: VerifyEmailComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AuthRoutingModule {}
