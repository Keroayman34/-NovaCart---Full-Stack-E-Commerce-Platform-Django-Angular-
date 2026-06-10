import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Cart } from '../../shared/models/cart.model';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = `${environment.apiUrl}/cart`;

  constructor(private http: HttpClient) {}

  getCart(): Observable<Cart> {
    return this.http.get<Cart>(`${this.apiUrl}/`);
  }

  addToCart(productId: number, quantity: number = 1): Observable<Cart> {
    return this.http.post<Cart>(`${this.apiUrl}/`, { product_id: productId, quantity });
  }

  updateCartItem(itemId: number, quantity: number): Observable<Cart> {
    return this.http.patch<Cart>(`${this.apiUrl}/items/${itemId}/`, { quantity });
  }

  removeCartItem(itemId: number): Observable<{message: string}> {
    return this.http.delete<{message: string}>(`${this.apiUrl}/items/${itemId}/`);
  }

  clearCart(): Observable<{message: string}> {
    return this.http.delete<{message: string}>(`${this.apiUrl}/clear/`);
  }
}