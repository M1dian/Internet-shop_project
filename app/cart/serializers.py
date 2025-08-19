"""
Cart serializers for the shop.
"""
from rest_framework import serializers
from .models import CartItem
from app.products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Cart item serializer.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'quantity',
            'total_price', 'added_at', 'updated_at'
        ]
        read_only_fields = ['id', 'added_at', 'updated_at']


class CartItemCreateSerializer(serializers.ModelSerializer):
    """
    Cart item create serializer.
    """
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть положительным")
        return value

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']
        
        if not product.is_active:
            raise serializers.ValidationError("Товар не активен")
        
        if not product.has_sufficient_stock(quantity):
            raise serializers.ValidationError(
                f"Недостаточно товара на складе. Доступно: {product.stock_quantity}"
            )
        
        return attrs


class CartItemUpdateSerializer(serializers.ModelSerializer):
    """
    Cart item update serializer.
    """
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть положительным")
        return value

    def validate(self, attrs):
        quantity = attrs['quantity']
        product = self.instance.product
        
        if not product.has_sufficient_stock(quantity):
            raise serializers.ValidationError(
                f"Недостаточно товара на складе. Доступно: {product.stock_quantity}"
            )
        
        return attrs


class CartSummarySerializer(serializers.Serializer):
    """
    Cart summary serializer.
    """
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = CartItemSerializer(many=True) 