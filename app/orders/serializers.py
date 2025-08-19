"""
Order serializers for the shop.
"""
from rest_framework import serializers
from .models import Order, OrderItem
from app.products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order item serializer.
    """
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'quantity',
            'price', 'total_price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer.
    """
    order_items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'status_display', 'total_amount',
            'items_count', 'order_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """
    Order creation serializer.
    """
    def validate(self, attrs):
        user = self.context['request'].user
        
        # Проверяем корзину
        from app.cart.models import CartItem
        cart_items = CartItem.objects.filter(user=user)
        
        if not cart_items.exists():
            raise serializers.ValidationError("Корзина пуста")
        
        # Проверяем баланс
        total_amount = sum(item.total_price for item in cart_items)
        if not user.has_sufficient_balance(total_amount):
            raise serializers.ValidationError(
                f"Недостаточно средств на балансе. Требуется: {total_amount} руб."
            )
        
        # Проверяем доступность товаров
        for item in cart_items:
            if not item.can_be_ordered():
                raise serializers.ValidationError(
                    f"Товар {item.product.name} недоступен для заказа"
                )
        
        return attrs


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Order status update serializer (admin only).
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError("Неверный статус заказа")
        return value


class OrderSummarySerializer(serializers.Serializer):
    """
    Order summary serializer.
    """
    total_orders = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_orders = serializers.IntegerField() 