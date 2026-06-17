import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { Category, Product, ProductListResponse, Review } from "../../shared/models/product.model";

@Injectable({
  providedIn: "root",
})
export class ProductsService {
  private readonly apiUrl = environment.apiUrl || "";

  constructor(private http: HttpClient) {}

  getProducts(params?: {
    search?: string;
    category?: number;
    category_slug?: string;
    price_min?: number;
    price_max?: number;
    in_stock?: boolean;
    ordering?: string;
    page?: number;
    page_size?: number;
  }): Observable<ProductListResponse> {
    let httpParams = new HttpParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          httpParams = httpParams.set(key, String(value));
        }
      });
    }
    return this.http.get<ProductListResponse>(`${this.apiUrl}/products/`, {
      params: httpParams,
    });
  }

  getProduct(id: number): Observable<{ success: boolean; data: Product }> {
    return this.http.get<{ success: boolean; data: Product }>(
      `${this.apiUrl}/products/${id}/`,
    );
  }

  getCategories(): Observable<{ success: boolean; data: { results: Category[] } }> {
    return this.http.get<{ success: boolean; data: { results: Category[] } }>(
      `${this.apiUrl}/categories/`,
    );
  }

  getReviews(productId: number): Observable<Review[]> {
    return this.http.get<Review[]>(
      `${this.apiUrl}/products/${productId}/reviews/`,
    );
  }

  addReview(productId: number, data: {
    rating: number;
    comment: string;
  }): Observable<Review> {
    return this.http.post<Review>(
      `${this.apiUrl}/products/${productId}/reviews/`,
      data,
    );
  }

  deleteReview(reviewId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/reviews/${reviewId}/`);
  }

  addToWishlist(productId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/wishlist/`, {
      product_id: productId,
    });
  }
}