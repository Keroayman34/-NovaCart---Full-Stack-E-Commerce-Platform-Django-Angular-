export interface Product {
  id: number;
  name: string;
  price: number;
  image?: string;
  primary_image?: {
    id: number;
    image: string;
    is_primary: boolean;
    alt_text: string;
  } | null;
}
