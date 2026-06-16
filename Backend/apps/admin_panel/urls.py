from django.urls import path

from .views.users import (
    AdminUserListView,
    AdminUserUpdateView,
    AdminUserDeleteView,
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

]