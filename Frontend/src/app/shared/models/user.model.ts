export interface UserProfile {
  id?: number;
  email: string;
  phone: string;
  role: string;
  is_verified: boolean;
  avatar: string | null;
}

export interface Address {
  id?: number;
  street: string;
  city: string;
  country: string;
}
