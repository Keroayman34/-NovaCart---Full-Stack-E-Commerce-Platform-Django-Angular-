import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SellerProductService, Product, Category } from '../../../core/services/seller-product.service';

@Component({
  selector: 'app-seller-products',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './seller-products.component.html',
  styleUrls: ['./seller-products.component.scss'],
})
export class SellerProductsComponent implements OnInit {
  products: Product[] = [];
  categories: Category[] = [];
  loading = true;
  searchQuery = '';

  showModal = false;
  isEditing = false;
  editingProductId: number | null = null;
  saving = false;
  error = '';

  formData = {
    name: '',
    description: '',
    sku: '',
    price: 0,
    stock_quantity: 0,
    category_id: 0,
    is_active: true,
  };

  selectedFile: File | null = null;
  previewUrl: string | null = null;

  deletingProductId: number | null = null;
  showDeleteConfirm = false;

  constructor(private service: SellerProductService) {}

  ngOnInit(): void {
    this.loadProducts();
    this.loadCategories();
  }

  get filteredProducts(): Product[] {
    if (!this.searchQuery.trim()) return this.products;
    const q = this.searchQuery.toLowerCase();
    return this.products.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.sku.toLowerCase().includes(q) ||
        p.category_name.toLowerCase().includes(q)
    );
  }

  loadProducts(): void {
    this.loading = true;
    this.service.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadCategories(): void {
    this.service.getCategories().subscribe({
      next: (data) => {
        this.categories = data;
      },
    });
  }

  openCreateModal(): void {
    this.isEditing = false;
    this.editingProductId = null;
    this.formData = { name: '', description: '', sku: '', price: 0, stock_quantity: 0, category_id: 0, is_active: true };
    this.selectedFile = null;
    this.previewUrl = null;
    this.error = '';
    this.showModal = true;
  }

  openEditModal(product: Product): void {
    this.isEditing = true;
    this.editingProductId = product.id;
    this.formData = {
      name: product.name,
      description: product.description || '',
      sku: product.sku,
      price: Number(product.price),
      stock_quantity: product.stock_quantity,
      category_id: product.category_id,
      is_active: product.is_active,
    };
    this.selectedFile = null;
    this.previewUrl = null;
    this.error = '';
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.error = '';
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

  saveProduct(): void {
    if (!this.formData.name || !this.formData.sku || !this.formData.price || !this.formData.category_id) {
      this.error = 'Name, SKU, price, and category are required.';
      return;
    }

    this.saving = true;
    this.error = '';

    const fd = new FormData();
    fd.append('name', this.formData.name);
    fd.append('description', this.formData.description);
    fd.append('sku', this.formData.sku);
    fd.append('price', String(this.formData.price));
    fd.append('stock_quantity', String(this.formData.stock_quantity));
    fd.append('category_id', String(this.formData.category_id));
    fd.append('is_active', String(this.formData.is_active));
    if (this.selectedFile) {
      fd.append('image', this.selectedFile);
    }

    const request = this.isEditing && this.editingProductId
      ? this.service.updateProduct(this.editingProductId, fd)
      : this.service.createProduct(fd);

    request.subscribe({
      next: () => {
        this.saving = false;
        this.closeModal();
        this.loadProducts();
      },
      error: (err) => {
        this.saving = false;
        if (err.error && typeof err.error === 'object') {
          const messages = Object.values(err.error).flat().join('; ');
          this.error = messages || 'Failed to save product.';
        } else {
          this.error = 'Failed to save product.';
        }
      },
    });
  }

  confirmDelete(product: Product): void {
    this.deletingProductId = product.id;
    this.showDeleteConfirm = true;
  }

  cancelDelete(): void {
    this.deletingProductId = null;
    this.showDeleteConfirm = false;
  }

  executeDelete(): void {
    if (!this.deletingProductId) return;
    this.service.deleteProduct(this.deletingProductId).subscribe({
      next: () => {
        this.showDeleteConfirm = false;
        this.deletingProductId = null;
        this.loadProducts();
      },
      error: () => {
        this.showDeleteConfirm = false;
        this.deletingProductId = null;
      },
    });
  }

  formatPrice(price: string): string {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(price));
  }

  getStatusClass(product: Product): string {
    if (!product.is_active) return 'inactive';
    if (Number(product.stock_quantity) === 0) return 'out-of-stock';
    return 'active';
  }

  getStatusLabel(product: Product): string {
    if (!product.is_active) return 'Inactive';
    if (Number(product.stock_quantity) === 0) return 'Out of Stock';
    return 'Active';
  }

  getPrimaryImage(product: Product): string | null {
    const primary = product.images?.find((img) => img.is_primary);
    return primary?.image || (product.images?.[0]?.image ?? null);
  }
}
