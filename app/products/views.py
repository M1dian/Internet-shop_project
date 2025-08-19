"""
Product views for the shop.
"""
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import (
    ProductSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer
)


class ProductListView(generics.ListAPIView):
    """
    Product list view - accessible to all users.
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """
    Product detail view - accessible to all users.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductCreateView(generics.CreateAPIView):
    """
    Product create view - admin only.
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    """
    Product update view - admin only.
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class ProductDeleteView(generics.DestroyAPIView):
    """
    Product delete view - admin only.
    """
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response({'message': 'Товар успешно деактивирован'}, status=status.HTTP_200_OK)


class CategoryListView(generics.ListAPIView):
    """
    Category list view - accessible to all users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductStockInfoView(APIView):
    """
    Get product stock information.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        return Response({
            'id': product.id,
            'name': product.name,
            'stock_quantity': product.stock_quantity,
            'is_in_stock': product.is_in_stock(),
            'price': product.price
        }, status=status.HTTP_200_OK)