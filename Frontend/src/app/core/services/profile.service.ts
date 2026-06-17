import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { Address, UserProfile } from "../../shared/models/user.model";
import { Product } from "../../shared/models/product.model";
import { Order } from "../../shared/models/order.model";

@Injectable({
  providedIn: "root",
})
export class ProfileService {
  private readonly apiUrl = environment.apiUrl || "";

  constructor(private http: HttpClient) {}

  getUserProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/profile/`);
  }

  updateProfile(payload: Partial<UserProfile>): Observable<UserProfile> {
    return this.http.patch<UserProfile>(`${this.apiUrl}/profile/`, payload);
  }

  getAddresses(): Observable<Address[]> {
    return this.http.get<Address[]>(`${this.apiUrl}/profile/addresses/`);
  }

  addAddress(payload: Address): Observable<Address> {
    return this.http.post<Address>(`${this.apiUrl}/profile/addresses/`, payload);
  }

  updateAddress(id: number, payload: Address): Observable<Address> {
    return this.http.put<Address>(
      `${this.apiUrl}/profile/addresses/${id}/`,
      payload,
    );
  }

  deleteAddress(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/profile/addresses/${id}/`);
  }

  getWishlist(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/wishlist/`);
  }

  removeFromWishlist(productId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/wishlist/${productId}/`);
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.apiUrl}/orders/`);
  }

  getOrder(id: number): Observable<Order> {
    return this.http.get<Order>(`${this.apiUrl}/orders/${id}/`);
  }
}
