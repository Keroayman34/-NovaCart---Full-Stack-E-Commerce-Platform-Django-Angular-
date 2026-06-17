import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { ProductsService } from "../products.service";
import { AuthService } from "../../../core/services/auth.service";
import { Product, Review } from "../../../shared/models/product.model";

@Component({
  selector: "app-product-detail",
  templateUrl: "./product-detail.component.html",
  styleUrls: ["./product-detail.component.scss"],
})
export class ProductDetailComponent implements OnInit {
  product: Product | null = null;
  reviews: Review[] = [];
  isLoading = true;
  errorMessage = "";

  newRating = 5;
  newComment = "";
  isSubmittingReview = false;
  reviewErrorMessage = "";
  reviewSuccessMessage = "";

  activeImageIndex = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productsService: ProductsService,
    public authService: AuthService,
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get("id"));
    if (!id) {
      this.router.navigate(["/products"]);
      return;
    }
    this.loadProduct(id);
    this.loadReviews(id);
  }

  loadProduct(id: number): void {
    this.isLoading = true;
    this.errorMessage = "";

    this.productsService.getProduct(id).subscribe({
      next: (res) => {
        if (res.success && res.data) {
          this.product = res.data;
        } else {
          this.errorMessage = "Product not found.";
        }
      },
      error: () => {
        this.errorMessage = "Failed to load product.";
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  loadReviews(productId: number): void {
    this.productsService.getReviews(productId).subscribe({
      next: (data) => {
        this.reviews = data;
      },
    });
  }

  submitReview(): void {
    if (!this.product || !this.authService.isLoggedIn()) return;

    this.isSubmittingReview = true;
    this.reviewErrorMessage = "";
    this.reviewSuccessMessage = "";

    this.productsService
      .addReview(this.product.id, {
        rating: this.newRating,
        comment: this.newComment,
      })
      .subscribe({
        next: () => {
          this.reviewSuccessMessage = "Review submitted.";
          this.newRating = 5;
          this.newComment = "";
          this.loadReviews(this.product!.id);
          this.loadProduct(this.product!.id);
        },
        error: (err) => {
          this.reviewErrorMessage =
            err.error?.non_field_errors?.[0] ||
            err.error?.rating?.[0] ||
            "Failed to submit review.";
        },
        complete: () => {
          this.isSubmittingReview = false;
        },
      });
  }

  deleteReview(reviewId: number): void {
    this.productsService.deleteReview(reviewId).subscribe({
      next: () => {
        this.reviews = this.reviews.filter((r) => r.id !== reviewId);
        if (this.product) {
          this.loadProduct(this.product.id);
        }
      },
    });
  }

  addToWishlist(): void {
    if (!this.product || !this.authService.isLoggedIn()) return;
    this.productsService.addToWishlist(this.product.id).subscribe();
  }

  getImages(): string[] {
    if (!this.product?.images) return [];
    return this.product.images.map((img) => img.image);
  }
}