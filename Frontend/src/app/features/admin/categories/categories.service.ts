import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Category {
  id: number;
  name: string;
  description: string;
  slug: string;
  product_count: number;
  created_at: string;
  updated_at: string;
}

export interface CategoryListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Category[];
}

@Injectable({
  providedIn: 'root',
})
export class CategoriesService {
  private apiUrl = 'http://127.0.0.1:8000/api/admin/categories';

  constructor(private http: HttpClient) {}

  getCategories(page: number = 1, searchTerm?: string): Observable<CategoryListResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', '10');

    if (searchTerm && searchTerm.trim()) {
      params = params.set('search', searchTerm.trim());
    }

    return this.http.get<CategoryListResponse>(this.apiUrl, { params });
  }

  getCategory(categoryId: number): Observable<Category> {
    return this.http.get<Category>(`${this.apiUrl}/${categoryId}`);
  }

  createCategory(data: {
    name: string;
    description: string;
    slug: string;
  }): Observable<{ message: string; category: Category }> {
    return this.http.post<{ message: string; category: Category }>(this.apiUrl, data);
  }

  updateCategory(
    categoryId: number,
    data: { name: string; description: string; slug: string }
  ): Observable<{ message: string; category: Category }> {
    return this.http.put<{ message: string; category: Category }>(
      `${this.apiUrl}/${categoryId}/`,
      data
    );
  }

  deleteCategory(categoryId: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiUrl}/${categoryId}/`);
  }
}
