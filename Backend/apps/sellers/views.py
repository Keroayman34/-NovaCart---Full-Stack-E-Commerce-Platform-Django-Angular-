from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import SellerProfile
from .serializers import *
from apps.products.serializers import ProductSerializer
from apps.products.models import Product
from core.permissions import IsSeller


class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = [JSONParser, MultiPartParser, FormParser]


    def get(self, request):
        try:
            profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "No shop profile found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SellerProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateSellerProfileSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            profile = serializer.save()
            return Response(
                SellerProfileSerializer(profile, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "No shop profile found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CreateSellerProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                SellerProfileSerializer(profile, context={"request": request}).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SellerOwnerProductListView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        try:
            products = Product.objects.filter(seller=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "No shop profile found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SellerProductOwnerListSerializer(profile, context={"request": request})
        return Response(serializer.data)
    
class SellerOwnerProductDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)
    

class SellerOwnerProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller ]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product, context={"request": request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SellerOwnerProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SellerOwnerProductDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)