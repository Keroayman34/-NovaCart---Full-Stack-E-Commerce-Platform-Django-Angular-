export interface OrderItem {
  id: number;
  product: number;
  product_name: string;
  quantity: number;
  price: number;
  total: number;
}

export interface Order {
  id: number;
  user: string;
  status: string;
  total_price: number;
  address: string;
  items: OrderItem[];
  created_at: string;
}
