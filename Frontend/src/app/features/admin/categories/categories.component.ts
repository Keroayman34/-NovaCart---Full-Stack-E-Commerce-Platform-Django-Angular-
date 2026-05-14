import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CategoriesService, Category } from './categories.service';
import { CategoryFormComponent } from './category-form/category-form.component';

@Component({
  selector: 'app-admin-categories',
  standalone: true,
  imports: [CommonModule, FormsModule, CategoryFormComponent],
  templateUrl: './categories.component.html',
  styleUrls: ['./categories.component.scss'],
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
  loading = false;
  errorMessage = '';
  successMessage = '';

  // Pagination
  currentPage = 1;
  totalPages = 1;
  pageNumbers: number[] = [];

  // Search
  searchTerm = '';

  // Modal
  showForm = false;
  formMode: 'create' | 'edit' = 'create';
  selectedCategory: Category | null = null;

  constructor(private categoriesService: CategoriesService) {}

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(page: number = 1): void {
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.categoriesService.getCategories(page, this.searchTerm).subscribe({
      next: (response) => {
        this.categories = response.results;
        this.currentPage = page;
        this.totalPages = Math.ceil(response.count / 10);
        this.generatePageNumbers();
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load categories. Please try again.';
        this.loading = false;
      },
    });
  }

  generatePageNumbers(): void {
    this.pageNumbers = [];
    const maxPagesToShow = 5;
    let startPage = Math.max(1, this.currentPage - 2);
    let endPage = Math.min(this.totalPages, startPage + maxPagesToShow - 1);

    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      this.pageNumbers.push(i);
    }
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.loadCategories(page);
      window.scrollTo(0, 0);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.goToPage(this.currentPage - 1);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.goToPage(this.currentPage + 1);
    }
  }

  onSearch(): void {
    this.currentPage = 1;
    this.loadCategories();
  }

  resetSearch(): void {
    this.searchTerm = '';
    this.currentPage = 1;
    this.loadCategories();
  }

  openAddForm(): void {
    this.formMode = 'create';
    this.selectedCategory = null;
    this.showForm = true;
  }

  openEditForm(category: Category): void {
    this.formMode = 'edit';
    this.selectedCategory = category;
    this.showForm = true;
  }

  deleteCategory(category: Category): void {
    if (confirm(`Are you sure you want to delete the category "${category.name}"?`)) {
      this.loading = true;
      this.categoriesService.deleteCategory(category.id).subscribe({
        next: () => {
          this.successMessage = 'Category deleted successfully!';
          this.loadCategories(this.currentPage);
        },
        error: (error) => {
          this.errorMessage = 'Failed to delete category. Please try again.';
          this.loading = false;
        },
      });
    }
  }

  closeForm(): void {
    this.showForm = false;
    this.selectedCategory = null;
  }

  onFormSubmit(): void {
    this.successMessage =
      `Category ${this.formMode === 'create' ? 'created' : 'updated'} successfully!`;
    this.closeForm();
    this.loadCategories(this.currentPage);
  }
}
