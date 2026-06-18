import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ProductImage {
  id: number;
  image: string;
  is_primary: boolean;
  alt_text: string | null;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  sku: string;
  price: string;
  stock_quantity: number;
  average_rating: string;
  rating_count: number;
  is_in_stock: boolean;
  is_active: boolean;
  category_id: number;
  category_name: string;
  seller_id?: number;
  seller_name?: string;
  images: ProductImage[];
  url: string;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

@Injectable({ providedIn: 'root' })
export class SellerProductService {
  private apiUrl = `${environment.apiUrl}/sellers`;

  constructor(private http: HttpClient) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/products/`);
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/products/${id}/`);
  }

  createProduct(data: FormData): Observable<Product> {
    return this.http.post<Product>(`${this.apiUrl}/products/create/`, data);
  }

  updateProduct(id: number, data: FormData): Observable<Product> {
    return this.http.put<Product>(`${this.apiUrl}/products/${id}/update/`, data);
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/products/${id}/delete/`);
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${environment.apiUrl}/categories/`);
  }
}
