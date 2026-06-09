import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface Order {
  id: number;
  customer_id: number;
  customer_name: string;
  customer_email: string;
  total_amount: number;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
  payment_method: string;
  shipping_address: string;
  created_at: string;
  updated_at: string;
  items?: OrderItem[];
}

export interface OrderListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Order[];
}

@Injectable({
  providedIn: 'root',
})
export class OrdersService {
  private apiUrl = 'http://127.0.0.1:8000/api/admin/orders';

  constructor(private http: HttpClient) {}

  getOrders(
    page: number = 1,
    status?: string,
    searchTerm?: string
  ): Observable<OrderListResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', '10');

    if (status && status !== '') {
      params = params.set('status', status);
    }

    if (searchTerm && searchTerm.trim()) {
      params = params.set('search', searchTerm.trim());
    }

    return this.http.get<OrderListResponse>(this.apiUrl, { params });
  }

  getOrder(orderId: number): Observable<Order> {
    return this.http.get<Order>(`${this.apiUrl}/${orderId}`);
  }

  updateOrderStatus(
    orderId: number,
    status: string
  ): Observable<{ message: string; order: Order }> {
    return this.http.patch<{ message: string; order: Order }>(
      `${this.apiUrl}/${orderId}/status/`,
      { status }
    );
  }

  cancelOrder(orderId: number): Observable<{ message: string }> {
    return this.http.patch<{ message: string }>(
      `${this.apiUrl}/${orderId}/cancel/`,
      {}
    );
  }
}
