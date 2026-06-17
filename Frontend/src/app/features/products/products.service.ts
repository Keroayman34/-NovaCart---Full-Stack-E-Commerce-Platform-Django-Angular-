import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface Product {
  id: number;
  name: string;
  slug: string;
  sku: string;
  price: string;
  stock_quantity: number;
  is_in_stock: boolean;
  category_name: string;
  seller_name: string;
  primary_image: { id: number; image: string; is_primary: boolean; alt_text: string } | null;
  is_active: boolean;
  created_at: string;
}

export interface ProductDetail extends Product {
  description: string;
  category: { id: number; name: string; slug: string };
  seller_id: number;
  images: { id: number; image: string; is_primary: boolean; alt_text: string }[];
}

export interface ApiListResponse<T> {
  success: boolean;
  data: {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
  };
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface ProductFilters {
  search?: string;
  category?: number;
  min_price?: number;
  max_price?: number;
  ordering?: string;
  page?: number;
  page_size?: number;
}

@Injectable({ providedIn: 'root' })
export class ProductsService {
  private apiUrl = `${environment.apiUrl}/products`;
  private categoriesUrl = `${environment.apiUrl}/categories`;

  constructor(private http: HttpClient) {}

  getProducts(filters: ProductFilters = {}): Observable<ApiListResponse<Product>> {
    let params = new HttpParams();
    if (filters.search)    params = params.set('search', filters.search);
    if (filters.category)  params = params.set('category', filters.category.toString());
    if (filters.min_price) params = params.set('min_price', filters.min_price.toString());
    if (filters.max_price) params = params.set('max_price', filters.max_price.toString());
    if (filters.ordering)  params = params.set('ordering', filters.ordering);
    if (filters.page)      params = params.set('page', filters.page.toString());
    if (filters.page_size) params = params.set('page_size', filters.page_size.toString());

    return this.http.get<ApiListResponse<Product>>(this.apiUrl + '/', { params });
  }

  getProduct(id: number): Observable<ProductDetail> {
    return this.http.get<ProductDetail>(`${this.apiUrl}/${id}/`);
  }

  getCategories(): Observable<ApiListResponse<Category>> {
    return this.http.get<ApiListResponse<Category>>(this.categoriesUrl + '/');
  }
}
