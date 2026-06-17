export interface UserProfile {
  id?: number;
  name: string;
  email: string;
  phone?: string;
  role?: string;
  is_verified?: boolean;
  avatar?: string;
  first_name?: string;
  last_name?: string;
  is_active?: boolean;
}

export interface Address {
  id?: number;
  street: string;
  city: string;
  country: string;
}
