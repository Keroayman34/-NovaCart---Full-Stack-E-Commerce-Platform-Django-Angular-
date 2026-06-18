import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SellerProfileService, SellerProfile } from '../../../core/services/seller-profile.service';

@Component({
  selector: 'app-seller-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './seller-settings.component.html',
  styleUrls: ['./seller-settings.component.scss'],
})
export class SellerSettingsComponent implements OnInit {
  loading = true;
  saving = false;
  hasProfile = false;
  successMessage = '';
  errorMessage = '';

  formData = {
    shop_name: '',
    shop_description: '',
    address: '',
  };
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  currentLogo: string | null = null;

  constructor(private profileService: SellerProfileService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.loading = true;
    this.profileService.getProfile().subscribe({
      next: (profile) => {
        this.hasProfile = true;
        this.formData.shop_name = profile.shop_name;
        this.formData.shop_description = profile.shop_description || '';
        this.formData.address = profile.address || '';
        this.currentLogo = profile.shop_logo;
        this.previewUrl = null;
        this.selectedFile = null;
        this.loading = false;
      },
      error: () => {
        this.hasProfile = false;
        this.formData = { shop_name: '', shop_description: '', address: '' };
        this.currentLogo = null;
        this.loading = false;
      },
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewUrl = e.target?.result as string;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  removeLogo(): void {
    this.selectedFile = null;
    this.previewUrl = null;
  }

  saveSettings(): void {
    if (!this.formData.shop_name.trim()) {
      this.errorMessage = 'Shop name is required.';
      return;
    }

    this.saving = true;
    this.errorMessage = '';
    this.successMessage = '';

    const fd = new FormData();
    fd.append('shop_name', this.formData.shop_name);
    fd.append('shop_description', this.formData.shop_description);
    fd.append('address', this.formData.address);
    if (this.selectedFile) {
      fd.append('shop_logo', this.selectedFile);
    }

    const request = this.hasProfile
      ? this.profileService.updateProfile(fd)
      : this.profileService.createProfile(fd);

    request.subscribe({
      next: (profile) => {
        this.hasProfile = true;
        this.currentLogo = profile.shop_logo;
        this.selectedFile = null;
        this.previewUrl = null;
        this.saving = false;
        this.successMessage = 'Shop settings saved successfully.';
      },
      error: (err) => {
        this.saving = false;
        if (err.error && typeof err.error === 'object') {
          const msgs = Object.values(err.error).flat().join('; ');
          this.errorMessage = msgs || 'Failed to save settings.';
        } else {
          this.errorMessage = 'Failed to save settings.';
        }
      },
    });
  }
}
