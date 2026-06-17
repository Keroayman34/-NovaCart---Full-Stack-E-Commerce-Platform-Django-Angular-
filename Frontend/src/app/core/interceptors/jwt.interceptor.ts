import {
    HttpEvent,
    HttpHandler,
    HttpInterceptor,
    HttpRequest,
    HttpErrorResponse,
} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { AuthService } from "../services/auth.service";

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    const isApiUrl = request.url.startsWith("http://localhost:8000/api") || 
                     request.url.startsWith("/api");

    if (isApiUrl) {
      // Check if token is expired before attaching
      if (token && !this.isTokenExpired(token)) {
        request = request.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        });
      } else {
        // Token is expired or missing — clear it and send anonymous
        if (token) {
          this.authService.logout();
        }
        request = request.clone({
          withCredentials: true,
        });
      }
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401 && isApiUrl) {
          // Token was rejected by server — clear and logout
          this.authService.logout();
        }
        return throwError(() => error);
      })
    );
  }

  private isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.exp) {
        return Date.now() >= payload.exp * 1000;
      }
      return false;
    } catch {
      return true; // malformed token = treat as expired
    }
  }
}
