import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
} from "@angular/core";
import { FormBuilder, Validators } from "@angular/forms";
import { Address } from "../../../../shared/models/user.model";

@Component({
  selector: "app-address-form",
  templateUrl: "./address-form.component.html",
  styleUrls: ["./address-form.component.scss"],
})
export class AddressFormComponent implements OnChanges {
  @Input() address: Address | null = null;
  @Output() save = new EventEmitter<Address>();
  @Output() cancel = new EventEmitter<void>();

  addressForm = this.formBuilder.group({
    street: ["", [Validators.required]],
    city: ["", [Validators.required]],
    country: ["", [Validators.required]],
  });

  constructor(private formBuilder: FormBuilder) {}

  ngOnChanges(): void {
    if (this.address) {
      this.addressForm.patchValue({
        street: this.address.street,
        city: this.address.city,
        country: this.address.country,
      });
      return;
    }

    this.addressForm.reset();
  }

  // submit address form
  onSubmit(): void {
    if (this.addressForm.invalid) {
      this.addressForm.markAllAsTouched();
      return;
    }

    this.save.emit(this.addressForm.value as Address);
  }

  // cancel edit
  onCancel(): void {
    this.cancel.emit();
  }
}
