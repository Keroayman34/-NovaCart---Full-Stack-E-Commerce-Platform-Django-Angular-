export interface OrderItem {
  id: number;
  product: number;
  product_name: string;
  price: number;
  quantity: number;
  total: number;
}

export interface Order {
  id: number;
  user: string;
  status: string;
  total_price: string;
  address: string;
  created_at: string;
  items: OrderItem[];
}
