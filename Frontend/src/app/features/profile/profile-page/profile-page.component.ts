import { Component, OnInit } from "@angular/core";
import { FormBuilder, Validators } from "@angular/forms";
import { ProfileService } from "../../../core/services/profile.service";
import { UserProfile } from "../../../shared/models/user.model";

@Component({
  selector: "app-profile-page",
  templateUrl: "./profile-page.component.html",
  styleUrls: ["./profile-page.component.scss"],
})
export class ProfilePageComponent implements OnInit {
  profile?: UserProfile;
  isLoading = true;
  isSaving = false;
  successMessage = "";
  errorMessage = "";

  profileForm = this.formBuilder.group({
    name: ["", [Validators.required]],
    email: ["", [Validators.required, Validators.email]],
  });

  constructor(
    private formBuilder: FormBuilder,
    private profileService: ProfileService,
  ) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  // fetch user profile
  loadProfile(): void {
    this.isLoading = true;
    this.errorMessage = "";

    this.profileService.getUserProfile().subscribe({
      next: (profile) => {
        this.profile = profile;
        this.profileForm.patchValue({
          name: profile.name,
          email: profile.email,
        });
      },
      error: () => {
        this.errorMessage = "Unable to load profile.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  // update profile data
  onSubmit(): void {
    this.successMessage = "";
    this.errorMessage = "";

    if (this.profileForm.invalid) {
      this.profileForm.markAllAsTouched();
      return;
    }

    this.isSaving = true;

    this.profileService.updateProfile(this.profileForm.value).subscribe({
      next: (profile) => {
        this.profile = profile;
        this.successMessage = "Profile updated successfully.";
      },
      error: () => {
        this.errorMessage = "Unable to update profile.";
      },
      complete: () => {
        this.isSaving = false;
      },
    });
  }
}
