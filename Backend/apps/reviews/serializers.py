from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_email', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user_email', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("الـ rating لازم يكون بين 1 و 5.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("انت عملت review على المنتج ده قبل كده.")
        return data