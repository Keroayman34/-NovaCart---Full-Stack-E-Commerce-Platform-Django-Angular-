import { Component, OnInit } from "@angular/core";
import { ProductsService } from "../products.service";
import { Category, Product } from "../../../shared/models/product.model";

@Component({
  selector: "app-product-list",
  templateUrl: "./product-list.component.html",
  styleUrls: ["./product-list.component.scss"],
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  categories: Category[] = [];
  isLoading = true;
  errorMessage = "";

  searchTerm = "";
  selectedCategory = "";
  minPrice: number | null = null;
  maxPrice: number | null = null;
  inStockOnly = false;
  sortBy = "-created_at";

  currentPage = 1;
  totalPages = 1;
  totalItems = 0;
  pageSize = 10;

  constructor(private productsService: ProductsService) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadProducts();
  }

  loadCategories(): void {
    this.productsService.getCategories().subscribe({
      next: (res) => {
        this.categories = res.data?.results || [];
      },
    });
  }

  loadProducts(): void {
    this.isLoading = true;
    this.errorMessage = "";

    const params: any = { page: this.currentPage, page_size: this.pageSize };
    if (this.searchTerm) params.search = this.searchTerm;
    if (this.selectedCategory) params.category = Number(this.selectedCategory);
    if (this.minPrice !== null) params.price_min = this.minPrice;
    if (this.maxPrice !== null) params.price_max = this.maxPrice;
    if (this.inStockOnly) params.in_stock = true;
    if (this.sortBy) params.ordering = this.sortBy;

    this.productsService.getProducts(params).subscribe({
      next: (res) => {
        if (res.success && res.data) {
          this.products = res.data.results || [];
          this.totalPages = res.data.pagination?.total_pages || 1;
          this.totalItems = res.data.pagination?.total_items || 0;
          this.currentPage = res.data.pagination?.current_page || 1;
        } else {
          this.products = [];
        }
      },
      error: () => {
        this.errorMessage = "Failed to load products.";
        this.products = [];
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  onSearch(): void {
    this.currentPage = 1;
    this.loadProducts();
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadProducts();
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this.loadProducts();
  }

  clearFilters(): void {
    this.searchTerm = "";
    this.selectedCategory = "";
    this.minPrice = null;
    this.maxPrice = null;
    this.inStockOnly = false;
    this.sortBy = "-created_at";
    this.currentPage = 1;
    this.loadProducts();
  }

  getPrimaryImage(product: Product): string | null {
    if (product.images && product.images.length > 0) {
      const primary = product.images.find((img) => img.is_primary);
      return primary ? primary.image : product.images[0].image;
    }
    return null;
  }
}