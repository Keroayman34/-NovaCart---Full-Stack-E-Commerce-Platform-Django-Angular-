import { Component } from "@angular/core";
import { FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { AuthService } from "../../../core/services/auth.service";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.scss"],
})
export class LoginComponent {
  errorMessage = "";
  isSubmitting = false;

  loginForm = this.formBuilder.group({
    email: ["", [Validators.required, Validators.email]],
    password: ["", [Validators.required]],
  });

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {}

  // handle login request
  onSubmit(): void {
    this.errorMessage = "";

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;

    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        // redirect after login
        this.router.navigate(["/products"]);
      },
      error: (err) => {
        // extract specific error message if available
        if (err.error && typeof err.error === 'object') {
          const firstKey = Object.keys(err.error)[0];
          if (firstKey && Array.isArray(err.error[firstKey])) {
            const msg = err.error[firstKey][0];
            if (msg.toLowerCase().includes('no active account')) {
              this.errorMessage = "Account not verified. Please check your email for the verification link.";
            } else {
              this.errorMessage = msg;
            }
          } else if (firstKey && typeof err.error[firstKey] === 'string') {
            const msg = err.error[firstKey];
            if (msg.toLowerCase().includes('no active account')) {
              this.errorMessage = "Account not verified. Please check your email for the verification link.";
            } else {
              this.errorMessage = msg;
            }
          } else {
            this.errorMessage = "Invalid email or password.";
          }
        } else {
          this.errorMessage = "Invalid email or password.";
        }
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      },
    });
  }
}
