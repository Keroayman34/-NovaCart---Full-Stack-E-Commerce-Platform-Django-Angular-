import { Component } from "@angular/core";
import { FormBuilder, Validators, AbstractControl, ValidationErrors } from "@angular/forms";
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
    email: ["", [Validators.required, Validators.email]],
    password: ["", [Validators.required, Validators.minLength(8)]],
    confirmPassword: ["", [Validators.required]],
    role: ["customer"],
    phone: [""],
  }, { validators: this.passwordMatchValidator });

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password')?.value;
    const confirmPassword = control.get('confirmPassword')?.value;
    // Only return mismatch if confirmPassword has been typed in
    if (confirmPassword && password !== confirmPassword) {
      return { mismatch: true };
    }
    return null;
  }

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {}

  registrationSuccess = false;

  // handle register request
  onSubmit(): void {
    this.errorMessage = "";

    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        // Show success message instead of navigating
        this.registrationSuccess = true;
      },
      error: (err) => {
        if (err.error && typeof err.error === 'object') {
          const firstKey = Object.keys(err.error)[0];
          if (firstKey && Array.isArray(err.error[firstKey])) {
            // E.g. {"email": ["A user with this email already exists."]}
            this.errorMessage = err.error[firstKey][0];
          } else if (firstKey && typeof err.error[firstKey] === 'string') {
            // E.g. {"detail": "Something went wrong."}
            this.errorMessage = err.error[firstKey];
          } else {
            this.errorMessage = "Unable to create account.";
          }
        } else {
          this.errorMessage = "Unable to create account. Please try again.";
        }
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      },
    });
  }
}
