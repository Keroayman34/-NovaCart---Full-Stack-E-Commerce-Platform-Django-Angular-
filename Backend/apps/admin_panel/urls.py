from django.urls import path

from .views.users import (
    AdminUserListView,
    AdminUserUpdateView,
    AdminUserDeleteView,
)

from .views.products import (
    AdminCategoryListView,
    AdminCategoryCreateView,
    AdminCategoryDetailView,
    AdminProductListView,
    AdminProductSoftDeleteView,
)

from .views.orders import (
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderStatusUpdateView,
    AdminCancelOrderView,
)

urlpatterns = [

    # Users

    path(
        "users/",
        AdminUserListView.as_view(),
        name="admin-users-list"
    ),

    path(
        "users/<int:pk>/",
        AdminUserUpdateView.as_view(),
        name="admin-user-update"
    ),

    path(
        "users/<int:pk>/delete/",
        AdminUserDeleteView.as_view(),
        name="admin-user-delete"
    ),

    # Categories

    path(
        "categories/",
        AdminCategoryListView.as_view(),
        name="admin-category-list"
    ),

    path(
        "categories/create/",
        AdminCategoryCreateView.as_view(),
        name="admin-category-create"
    ),

    path(
        "categories/<int:pk>/",
        AdminCategoryDetailView.as_view(),
        name="admin-category-detail"
    ),

    # Products

    path(
        "products/",
        AdminProductListView.as_view(),
        name="admin-product-list"
    ),

    path(
        "products/<int:pk>/delete/",
        AdminProductSoftDeleteView.as_view(),
        name="admin-product-delete"
    ),

    # Orders

    path(
        "orders/",
        AdminOrderListView.as_view(),
        name="admin-orders-list"
    ),

    path(
        "orders/<int:order_id>/",
        AdminOrderDetailView.as_view(),
        name="admin-order-detail"
    ),

    path(
        "orders/<int:order_id>/update-status/",
        AdminOrderStatusUpdateView.as_view(),
        name="admin-order-update-status"
    ),

    path(
        "orders/<int:order_id>/cancel/",
        AdminCancelOrderView.as_view(),
        name="admin-order-cancel"
    ),

]