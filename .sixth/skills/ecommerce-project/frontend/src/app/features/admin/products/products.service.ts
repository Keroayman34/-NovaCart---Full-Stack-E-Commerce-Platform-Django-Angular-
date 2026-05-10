import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../../../environments/environment";

export interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
  image_url: string;
  seller?: string | null;
  created_at: string;
  is_deleted: boolean;
}

export interface ProductListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

export interface ProductCreatePayload {
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
  image_url?: string;
}

@Injectable({
  providedIn: "root",
})
export class AdminProductsService {
  private apiUrl = environment.apiUrl || "";

  constructor(private http: HttpClient) {}

  // Get all products (admin view) with optional filters
  getProducts(page: number = 1): Observable<ProductListResponse> {
    const params = new HttpParams().set("page", page.toString());

    return this.http.get<ProductListResponse>(`${this.apiUrl}/admin/products/`, {
      params,
    });
  }

  // Get single product
  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/admin/products/${id}/`);
  }

  // Create product
  createProduct(payload: ProductCreatePayload): Observable<Product> {
    return this.http.post<Product>(`${this.apiUrl}/admin/products/`, payload);
  }

  // Update product
  updateProduct(id: number, payload: Partial<ProductCreatePayload>): Observable<Product> {
    return this.http.put<Product>(`${this.apiUrl}/admin/products/${id}/`, payload);
  }

  // Delete product (soft delete)
  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/products/${id}/`);
  }
}
