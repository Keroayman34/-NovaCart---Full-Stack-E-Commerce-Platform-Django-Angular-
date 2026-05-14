import { Component } from "@angular/core";
import { FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { AuthService } from "../../../core/services/auth.service";

@Component({
  selector: "app-register",
  templateUrl: "./register.component.html",
  styleUrls: ["./register.component.scss"],
})
export class RegisterComponent {
  errorMessage = "";
  isSubmitting = false;

  registerForm = this.formBuilder.group({
    name: ["", [Validators.required]],
    email: ["", [Validators.required, Validators.email]],
    password: ["", [Validators.required]],
    confirmPassword: ["", [Validators.required]],
  });

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {}

  // handle register request
  onSubmit(): void {
    this.errorMessage = "";

    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    if (
      this.registerForm.value.password !==
      this.registerForm.value.confirmPassword
    ) {
      this.errorMessage = "Passwords do not match.";
      return;
    }

    this.isSubmitting = true;

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        // go to login after success
        this.router.navigate(["/login"]);
      },
      error: () => {
        this.errorMessage = "Unable to create account.";
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      },
    });
  }
}
