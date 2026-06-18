import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface SellerProfile {
  id: number;
  user: {
    id: number;
    email: string;
    name: string;
  };
  shop_name: string;
  shop_description: string;
  shop_logo: string | null;
  address: string;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class SellerProfileService {
  private apiUrl = `${environment.apiUrl}/sellers/profile/`;

  constructor(private http: HttpClient) {}

  getProfile(): Observable<SellerProfile> {
    return this.http.get<SellerProfile>(this.apiUrl);
  }

  createProfile(data: FormData): Observable<SellerProfile> {
    return this.http.post<SellerProfile>(this.apiUrl, data);
  }

  updateProfile(data: FormData): Observable<SellerProfile> {
    return this.http.patch<SellerProfile>(this.apiUrl, data);
  }
}
