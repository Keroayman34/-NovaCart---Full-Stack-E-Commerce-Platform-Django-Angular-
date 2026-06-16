from rest_framework import serializers
from .models import *
from apps.orders.models import Order

class AdminUpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)