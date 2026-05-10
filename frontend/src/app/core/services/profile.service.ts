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

  // fetch user profile
  getUserProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/profile`);
  }

  // update profile data
  updateProfile(payload: Partial<UserProfile>): Observable<UserProfile> {
    return this.http.put<UserProfile>(`${this.apiUrl}/profile`, payload);
  }

  // load user addresses
  getAddresses(): Observable<Address[]> {
    return this.http.get<Address[]>(`${this.apiUrl}/profile/addresses`);
  }

  // add new address
  addAddress(payload: Address): Observable<Address> {
    return this.http.post<Address>(`${this.apiUrl}/profile/addresses`, payload);
  }

  // update existing address
  updateAddress(id: number, payload: Address): Observable<Address> {
    return this.http.put<Address>(
      `${this.apiUrl}/profile/addresses/${id}`,
      payload,
    );
  }

  // delete address
  deleteAddress(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/profile/addresses/${id}`);
  }

  // load wishlist
  getWishlist(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/profile/wishlist`);
  }

  // remove item from wishlist
  removeFromWishlist(productId: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/profile/wishlist/${productId}`,
    );
  }

  // display order list
  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.apiUrl}/profile/orders`);
  }
}
