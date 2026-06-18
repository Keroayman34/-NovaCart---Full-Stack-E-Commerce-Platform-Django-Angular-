import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface SellerOrderItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  price: string;
  total: string;
}

export interface SellerOrder {
  id: number;
  customer: string;
  address: string;
  status: string;
  date: string;
  total_amount: string;
  items: SellerOrderItem[];
}

@Injectable({
  providedIn: 'root'
})
export class SellerOrderService {
  private apiUrl = `${environment.apiUrl}/sellers/orders/`;

  constructor(private http: HttpClient) {}

  getOrders(): Observable<SellerOrder[]> {
    return this.http.get<SellerOrder[]>(this.apiUrl);
  }

  updateOrderStatus(orderId: number, status: string): Observable<any> {
    return this.http.patch(`${environment.apiUrl}/orders/${orderId}/status/`, { status });
  }
}
