export interface OrderItem {
  id: number;
  productId: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

export interface Order {
  id: number;
  total: number;
  status: string;
  date: string;
  items: OrderItem[];
}
