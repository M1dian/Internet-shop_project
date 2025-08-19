"""
Product serializers for the shop.
"""
from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer for read operations.
    """
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock_quantity',
            'category', 'category_name', 'image', 'is_active',
            'created_at', 'updated_at', 'is_in_stock'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Product serializer for create/update operations (admin only).
    """
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'stock_quantity',
            'category', 'image', 'is_active'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество на складе не может быть отрицательным")
        return value 