from django.urls import include, path

urlpatterns = [
	path("api/payments/", include("apps.payments.urls")),
]
