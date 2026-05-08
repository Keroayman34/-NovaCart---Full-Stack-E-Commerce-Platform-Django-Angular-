import { Component, OnInit } from "@angular/core";
import { ProfileService } from "../../../core/services/profile.service";
import { Product } from "../../../shared/models/product.model";

@Component({
  selector: "app-wishlist",
  templateUrl: "./wishlist.component.html",
  styleUrls: ["./wishlist.component.scss"],
})
export class WishlistComponent implements OnInit {
  wishlist: Product[] = [];
  isLoading = true;
  errorMessage = "";

  constructor(private profileService: ProfileService) {}

  ngOnInit(): void {
    this.loadWishlist();
  }

  // load wishlist items
  loadWishlist(): void {
    this.isLoading = true;
    this.errorMessage = "";

    this.profileService.getWishlist().subscribe({
      next: (items) => {
        this.wishlist = items;
      },
      error: () => {
        this.errorMessage = "Unable to load wishlist.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  // remove item from wishlist
  onRemoveItem(productId: number): void {
    this.profileService.removeFromWishlist(productId).subscribe({
      next: () => {
        this.wishlist = this.wishlist.filter((item) => item.id !== productId);
      },
      error: () => {
        this.errorMessage = "Unable to remove item.";
      },
    });
  }
}
