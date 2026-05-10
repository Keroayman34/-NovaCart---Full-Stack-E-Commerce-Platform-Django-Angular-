import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../../../environments/environment";

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface UserListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: User[];
}

export interface UserUpdatePayload {
  is_active?: boolean;
  role?: string;
}

@Injectable({
  providedIn: "root",
})
export class AdminUsersService {
  private apiUrl = environment.apiUrl || "";

  constructor(private http: HttpClient) {}

  // Get all users with optional filters
  getUsers(
    page: number = 1,
    role?: string,
    status?: string,
  ): Observable<UserListResponse> {
    let params = new HttpParams();
    params = params.set("page", page.toString());

    if (role) {
      params = params.set("role", role);
    }

    if (status !== undefined && status !== "") {
      params = params.set("is_active", status === "active" ? "true" : "false");
    }

    return this.http.get<UserListResponse>(`${this.apiUrl}/admin/users/`, {
      params,
    });
  }

  // Update user status or role
  updateUser(userId: number, payload: UserUpdatePayload): Observable<User> {
    return this.http.patch<User>(`${this.apiUrl}/admin/users/${userId}/`, payload);
  }

  // Restrict/soft delete user
  restrictUser(userId: number): Observable<User> {
    return this.updateUser(userId, { is_active: false });
  }

  // Activate user
  activateUser(userId: number): Observable<User> {
    return this.updateUser(userId, { is_active: true });
  }
}
