from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id).select_related('user', 'product')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        data = request.data.copy()
        data['product'] = product_id
        serializer = ReviewSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            review = Review.objects.get(id=pk, user=request.user)
        except Review.DoesNotExist:
            return Response({'error': 'الـ review مش موجود.'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'message': 'الـ review اتحذف.'})
