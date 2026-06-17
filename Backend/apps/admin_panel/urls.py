from django.urls import path

from .views.users import (
    AdminUserListView,
    AdminUserUpdateView,
    AdminUserDeleteView,
)

from .views.orders import (
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderStatusUpdateView,
    AdminCancelOrderView,
)

urlpatterns = [

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