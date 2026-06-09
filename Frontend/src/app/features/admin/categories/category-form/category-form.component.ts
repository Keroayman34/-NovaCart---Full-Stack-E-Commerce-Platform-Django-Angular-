import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Category, CategoriesService } from '../categories.service';

@Component({
  selector: 'app-category-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './category-form.component.html',
  styleUrls: ['./category-form.component.scss'],
})
export class CategoryFormComponent implements OnInit {
  @Input() mode: 'create' | 'edit' = 'create';
  @Input() category: Category | null = null;
  @Output() formSubmitted = new EventEmitter<void>();
  @Output() formCancelled = new EventEmitter<void>();

  form!: FormGroup;
  loading = false;
  errorMessage = '';

  constructor(private fb: FormBuilder, private categoriesService: CategoriesService) {}

  ngOnInit(): void {
    this.initializeForm();
    if (this.mode === 'edit' && this.category) {
      this.populateForm();
    }
  }

  private initializeForm(): void {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      slug: ['', [Validators.required, Validators.pattern(/^[a-z0-9-]+$/)]],
    });
  }

  private populateForm(): void {
    if (this.category) {
      this.form.patchValue({
        name: this.category.name,
        description: this.category.description,
        slug: this.category.slug,
      });
    }
  }

  generateSlug(): void {
    const name = this.form.get('name')?.value || '';
    const slug = name
      .toLowerCase()
      .trim()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    this.form.patchValue({ slug });
  }

  onNameChange(): void {
    if (this.mode === 'create') {
      this.generateSlug();
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
    this.errorMessage = '';
    const formData = this.form.value;

    const request =
      this.mode === 'create'
        ? this.categoriesService.createCategory(formData)
        : this.categoriesService.updateCategory(this.category!.id, formData);

    request.subscribe({
      next: () => {
        this.loading = false;
        this.formSubmitted.emit();
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error.error?.message || 'Failed to save category. Please try again.';
      },
    });
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
    if (control.hasError('pattern')) {
      return `${this.formatLabel(fieldName)} can only contain lowercase letters, numbers, and hyphens`;
    }
    return '';
  }

  private formatLabel(fieldName: string): string {
    return fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
  }

  get formTitle(): string {
    return this.mode === 'create' ? 'Add New Category' : 'Edit Category';
  }

  get submitButtonText(): string {
    return this.mode === 'create' ? 'Create Category' : 'Update Category';
  }
}
