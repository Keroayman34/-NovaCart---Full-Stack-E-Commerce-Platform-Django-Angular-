import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, Observable, tap } from "rxjs";
import { environment } from "../../../environments/environment";

interface LoginPayload {
  email: string;
  password: string;
}

interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  confirmPassword?: string;
}

interface AuthResponse {
  token: string;
}

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private readonly tokenKey = "auth_token";
  private readonly apiUrl = environment.apiUrl || "";

  private loggedInSubject = new BehaviorSubject<boolean>(this.hasToken());
  private roleSubject = new BehaviorSubject<string | null>(
    this.getRoleFromToken(),
  );

  loggedIn$ = this.loggedInSubject.asObservable();
  role$ = this.roleSubject.asObservable();

  constructor(private http: HttpClient) {}

  // login user and store token
  login(payload: Partial<LoginPayload>): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${this.apiUrl}/auth/login`, payload)
      .pipe(
        tap((response) => {
          this.storeToken(response.token);
        }),
      );
  }

  // register new user
  register(payload: Partial<RegisterPayload>): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}/auth/register`,
      payload,
    );
  }

  // clear token and reset state
  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.loggedInSubject.next(false);
    this.roleSubject.next(null);
  }

  // check if user is logged in
  isLoggedIn(): boolean {
    return this.hasToken();
  }

  // return stored token
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  // read role from cached value
  getRole(): string | null {
    return this.roleSubject.value;
  }

  private storeToken(token: string): void {
    // store token after login
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
    return payload?.role || payload?.user?.role || null;
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
}
