from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_id', 'user_email', 'product', 'rating', 'comment', 'created_at', 'can_delete']
        read_only_fields = ['user_id', 'user_email', 'created_at', 'can_delete']

    def get_can_delete(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated and (obj.user_id == user.id or getattr(user, 'role', None) == 'admin'))

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('rating must be between 1 and 5.')
        return value

    def validate(self, data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        product = data.get('product')

        if user and user.is_authenticated and product and Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError('You have already reviewed this product.')
        return data
