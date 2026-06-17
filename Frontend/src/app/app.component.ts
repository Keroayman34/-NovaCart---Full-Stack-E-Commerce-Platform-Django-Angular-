import { Component } from "@angular/core";
import { Router, NavigationEnd } from "@angular/router";
import { filter } from "rxjs/operators";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent {
  showHeaderFooter = true;

  constructor(private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      // Hide global header and footer for seller and admin routes
      this.showHeaderFooter = !(event.urlAfterRedirects.includes('/seller') || event.urlAfterRedirects.includes('/admin'));
    });
  }
}
