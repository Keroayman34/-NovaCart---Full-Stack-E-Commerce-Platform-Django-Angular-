import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Product } from '../products.service';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.scss'],
})
export class ProductFormComponent implements OnInit {
  @Input() mode: 'create' | 'edit' = 'create';
  @Input() product: Product | null = null;
  @Output() formSubmitted = new EventEmitter<void>();
  @Output() formCancelled = new EventEmitter<void>();

  form!: FormGroup;
  loading = false;
  imagePreview: string | null = null;
  categories = [
    'Electronics',
    'Clothing',
    'Books',
    'Home & Garden',
    'Sports',
    'Toys',
    'Food & Groceries',
    'Beauty',
    'Other',
  ];

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.initializeForm();
    if (this.mode === 'edit' && this.product) {
      this.populateForm();
    }
  }

  private initializeForm(): void {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      category: ['', Validators.required],
      price: ['', [Validators.required, Validators.min(0.01)]],
      stock: ['', [Validators.required, Validators.min(0)]],
      image_url: [''],
    });
  }

  private populateForm(): void {
    if (this.product) {
      this.form.patchValue({
        name: this.product.name,
        description: this.product.description,
        category: this.product.category,
        price: this.product.price,
        stock: this.product.stock,
        image_url: this.product.image_url,
      });
      if (this.product.image_url) {
        this.imagePreview = this.product.image_url;
      }
    }
  }

  onImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target?.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  onSubmit(): void {
    if (this.form.invalid) {
      Object.keys(this.form.controls).forEach((key) => {
        const control = this.form.get(key);
        if (control && control.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    this.loading = true;
    // In a real app, you would submit the form data here
    // For now, we'll just emit the event after a short delay to simulate submission
    setTimeout(() => {
      this.loading = false;
      this.formSubmitted.emit();
    }, 500);
  }

  onCancel(): void {
    this.formCancelled.emit();
  }

  getErrorMessage(fieldName: string): string {
    const control = this.form.get(fieldName);
    if (!control || !control.errors || !control.touched) {
      return '';
    }

    if (control.hasError('required')) {
      return `${this.formatLabel(fieldName)} is required`;
    }
    if (control.hasError('minLength')) {
      const minLength = control.getError('minLength').requiredLength;
      return `${this.formatLabel(fieldName)} must be at least ${minLength} characters`;
    }
    if (control.hasError('min')) {
      return `${this.formatLabel(fieldName)} must be greater than 0`;
    }
    return '';
  }

  private formatLabel(fieldName: string): string {
    return fieldName.charAt(0).toUpperCase() + fieldName.slice(1).replace(/_/g, ' ');
  }

  get formTitle(): string {
    return this.mode === 'create' ? 'Add New Product' : 'Edit Product';
  }

  get submitButtonText(): string {
    return this.mode === 'create' ? 'Create Product' : 'Update Product';
  }
}
