import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil, debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { ProductsService, Product, Category } from '../products.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss'],
})
export class ProductListComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  categories: Category[] = [];
  loading = false;
  error: string | null = null;

  // Pagination
  totalCount = 0;
  currentPage = 1;
  pageSize = 16;

  // Filters
  searchControl = new FormControl('');
  selectedOrdering = '-created_at';
  selectedCategoryId: number | null = null;

  orderingOptions = [
    { value: '-created_at', label: 'Newest First' },
    { value: 'price',       label: 'Price: Low → High' },
    { value: '-price',      label: 'Price: High → Low' },
    { value: 'name',        label: 'Name A–Z' },
  ];

  private destroy$ = new Subject<void>();

  constructor(private productsService: ProductsService, private router: Router) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadProducts();

    this.searchControl.valueChanges.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.currentPage = 1;
      this.loadProducts();
    });
  }

  loadCategories(): void {
    this.productsService.getCategories().pipe(takeUntil(this.destroy$)).subscribe({
      next: (res) => {
        this.categories = res.data.results || [];
      },
      error: (err) => console.error('Failed to load categories', err)
    });
  }

  loadProducts(): void {
    this.loading = true;
    this.error = null;

    this.productsService.getProducts({
      search:    this.searchControl.value || undefined,
      ordering:  this.selectedOrdering,
      category:  this.selectedCategoryId || undefined,
      page:      this.currentPage,
      page_size: this.pageSize,
    }).pipe(takeUntil(this.destroy$)).subscribe({
      next: (res) => {
        this.products   = res.data.results;
        this.totalCount = res.data.count;
        this.loading    = false;
      },
      error: (err) => {
        this.error   = 'Failed to load products. Is the backend running?';
        this.loading = false;
        console.error(err);
      }
    });
  }

  onOrderingChange(): void {
    this.currentPage = 1;
    this.loadProducts();
  }

  onCategorySelect(categoryId: number | null): void {
    this.selectedCategoryId = categoryId;
    this.currentPage = 1;
    this.loadProducts();
  }

  goToDetail(id: number): void {
    this.router.navigate(['/products', id]);
  }

  get totalPages(): number {
    return Math.ceil(this.totalCount / this.pageSize);
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.loadProducts();
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadProducts();
    }
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
