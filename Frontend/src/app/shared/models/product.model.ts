export interface ProductImage {
  id: number;
  image: string;
  is_primary: boolean;
  alt_text?: string;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image?: string;
  is_active: boolean;
  products_count: number;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  sku: string;
  price: number;
  description?: string;
  stock_quantity: number;
  average_rating: number;
  rating_count: number;
  is_in_stock: boolean;
  is_active: boolean;
  category_id?: number;
  category_name?: string;
  category?: Category;
  seller_id?: number;
  seller_name?: string;
  images: ProductImage[];
  primary_image?: ProductImage;
  is_owned_by_user?: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ProductListResponse {
  success: boolean;
  data: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Product[];
    pagination: {
      total_items: number;
      total_pages: number;
      current_page: number;
      page_size: number;
    };
  };
}

export interface Review {
  id: number;
  user_id: number;
  user_email: string;
  product: number;
  rating: number;
  comment: string;
  created_at: string;
  can_delete: boolean;
}
