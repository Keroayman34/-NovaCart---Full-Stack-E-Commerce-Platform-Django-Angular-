import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, Observable, tap } from "rxjs";
import { environment } from "../../../environments/environment";

interface LoginPayload {
  email: string;
  password: string;
}

interface RegisterPayload {
  email: string;
  password: string;
  role?: string;
  phone?: string;
}

interface TokenResponse {
  access: string;
  refresh: string;
  role?: string;
  email?: string;
  is_verified?: boolean;
  user?: any;
}

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private readonly tokenKey = "auth_token";
  private readonly refreshTokenKey = "auth_refresh_token";
  private readonly apiUrl = environment.apiUrl || "";

  private loggedInSubject = new BehaviorSubject<boolean>(this.hasToken());
  private roleSubject = new BehaviorSubject<string | null>(
    this.getRoleFromToken(),
  );

  loggedIn$ = this.loggedInSubject.asObservable();
  role$ = this.roleSubject.asObservable();

  constructor(private http: HttpClient) {}

  login(payload: Partial<LoginPayload>): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(`${this.apiUrl}/token/`, payload)
      .pipe(
        tap((response) => {
          this.storeToken(response.access);
          if (response.refresh) {
            localStorage.setItem(this.refreshTokenKey, response.refresh);
          }
        }),
      );
  }

  register(payload: Partial<RegisterPayload>): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, payload);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshTokenKey);
    this.loggedInSubject.next(false);
    this.roleSubject.next(null);
  }

  isLoggedIn(): boolean {
    return this.hasToken();
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshTokenKey);
  }

  getRole(): string | null {
    return this.roleSubject.value;
  }

  private storeToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
    this.loggedInSubject.next(true);
    this.roleSubject.next(this.getRoleFromToken());
  }

  private hasToken(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }

  private getRoleFromToken(): string | null {
    const token = this.getToken();
    if (!token) {
      return null;
    }
    const payload = this.decodeToken(token);
    return payload?.role || null;
  }

  private decodeToken(token: string): any {
    try {
      const payload = token.split(".")[1];
      if (!payload) {
        return null;
      }
      const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
      const decoded = atob(normalized);
      return JSON.parse(decoded);
    } catch {
      return null;
    }
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}/profile/`);
  }
}
