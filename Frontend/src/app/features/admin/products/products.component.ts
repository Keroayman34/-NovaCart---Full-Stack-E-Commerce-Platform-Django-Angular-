import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { AdminProductsService, Product } from "./products.service";
import { ProductFormComponent } from "./product-form/product-form.component";

@Component({
  selector: "app-admin-products",
  standalone: true,
  imports: [CommonModule, ProductFormComponent],
  templateUrl: "./products.component.html",
  styleUrls: ["./products.component.scss"],
})
export class AdminProductsComponent implements OnInit {
  products: Product[] = [];
  isLoading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  // Modal state
  showForm = false;
  formMode: "create" | "edit" = "create";
  selectedProduct: Product | null = null;

  // Pagination
  currentPage = 1;
  totalCount = 0;
  pageSize = 10;

  constructor(private productsService: AdminProductsService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.isLoading = true;
    this.errorMessage = null;

    this.productsService.getProducts(this.currentPage).subscribe({
      next: (response) => {
        this.products = response.results;
        this.totalCount = response.count;
        this.isLoading = false;
      },
      error: (error) => {
        console.error("Failed to load products:", error);
        this.errorMessage = "Failed to load products. Please try again.";
        this.isLoading = false;
      },
    });
  }

  openAddForm(): void {
    this.formMode = "create";
    this.selectedProduct = null;
    this.showForm = true;
  }

  openEditForm(product: Product): void {
    this.formMode = "edit";
    this.selectedProduct = product;
    this.showForm = true;
  }

  closeForm(): void {
    this.showForm = false;
    this.selectedProduct = null;
  }

  onFormSubmit(): void {
    this.successMessage = `Product ${this.formMode === "create" ? "created" : "updated"} successfully!`;
    this.closeForm();
    this.loadProducts();
    setTimeout(() => {
      this.successMessage = null;
    }, 3000);
  }

  deleteProduct(product: Product): void {
    if (!confirm(`Are you sure you want to delete "${product.name}"? This action cannot be undone.`)) {
      return;
    }

    this.productsService.deleteProduct(product.id).subscribe({
      next: () => {
        this.successMessage = `Product "${product.name}" has been deleted.`;
        this.loadProducts();
        setTimeout(() => {
          this.successMessage = null;
        }, 3000);
      },
      error: (error) => {
        console.error("Failed to delete product:", error);
        this.errorMessage = `Failed to delete "${product.name}". Please try again.`;
      },
    });
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.getTotalPages()) return;
    this.currentPage = page;
    this.loadProducts();
  }

  getTotalPages(): number {
    return Math.ceil(this.totalCount / this.pageSize);
  }

  getPageNumbers(): number[] {
    const total = this.getTotalPages();
    const pages: number[] = [];
    const maxPagesToShow = 5;

    let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(total, startPage + maxPagesToShow - 1);

    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  }

  getImageUrl(product: Product): string {
    return product.image_url || "https://via.placeholder.com/60";
  }
}
