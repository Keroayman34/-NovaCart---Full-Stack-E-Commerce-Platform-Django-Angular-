import {
    HttpEvent,
    HttpHandler,
    HttpInterceptor,
    HttpRequest,
} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { AuthService } from "../services/auth.service";

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // Add auth header with jwt if user is logged in and request is to api url
    const token = this.authService.getToken();
    const isApiUrl = request.url.startsWith("http://localhost:8000/api") || 
                     request.url.startsWith("/api");

    if (isApiUrl) {
      if (token) {
        request = request.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        });
      } else {
        request = request.clone({
          withCredentials: true,
        });
      }
    }

    return next.handle(request);
  }
}
