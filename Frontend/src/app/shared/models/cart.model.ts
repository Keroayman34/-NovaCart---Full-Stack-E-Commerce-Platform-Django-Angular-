export interface CartItemProduct {
  id: number;
  name: string;
  price: string;
  primary_image: {
    id: number;
    image: string;
    is_primary: boolean;
    alt_text: string;
  } | null;
}

export interface CartItem {
  id: number;
  product: CartItemProduct;
  quantity: number;
  total: string;
}

export interface Cart {
  id: number;
  user: number | null;
  session_key: string | null;
  items: CartItem[];
  total_price: string;
  created_at: string;
  updated_at: string;
}