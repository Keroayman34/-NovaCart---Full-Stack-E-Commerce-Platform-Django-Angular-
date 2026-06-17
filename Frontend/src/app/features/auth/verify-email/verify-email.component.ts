import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { AuthService } from "../../../core/services/auth.service";

@Component({
  selector: "app-verify-email",
  templateUrl: "./verify-email.component.html",
  styleUrls: ["./verify-email.component.scss"],
})
export class VerifyEmailComponent implements OnInit {
  isVerifying = true;
  successMessage = "";
  errorMessage = "";

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const uid = this.route.snapshot.queryParamMap.get("uid");
    const token = this.route.snapshot.queryParamMap.get("token");

    if (uid && token) {
      this.verifyEmail(uid, token);
    } else {
      this.isVerifying = false;
      this.errorMessage = "Invalid verification link. Missing parameters.";
    }
  }

  private verifyEmail(uid: string, token: string): void {
    this.authService.verifyEmail(uid, token).subscribe({
      next: () => {
        this.isVerifying = false;
        this.router.navigate(["/login"]);
      },
      error: (err) => {
        this.isVerifying = false;
        if (err.error && typeof err.error === 'object') {
          const firstKey = Object.keys(err.error)[0];
          if (firstKey && Array.isArray(err.error[firstKey])) {
            this.errorMessage = err.error[firstKey][0];
          } else if (firstKey && typeof err.error[firstKey] === 'string') {
            this.errorMessage = err.error[firstKey];
          } else {
            this.errorMessage = "Verification failed. The link might be expired or invalid.";
          }
        } else {
          this.errorMessage = "Verification failed. The link might be expired or invalid.";
        }
      },
    });
  }
}
