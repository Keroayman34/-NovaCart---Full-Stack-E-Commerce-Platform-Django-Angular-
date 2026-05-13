from django.urls import path
from .views import NotificationListView, MarkAsReadView, MarkAllAsReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkAsReadView.as_view(), name='notification-read'),
    path('notifications/read-all/', MarkAllAsReadView.as_view(), name='notification-read-all'),
]