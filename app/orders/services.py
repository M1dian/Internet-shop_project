"""
Order services for the shop.
"""
import logging
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model
from app.cart.models import CartItem
from app.products.models import Product
from .models import Order, OrderItem

User = get_user_model()
logger = logging.getLogger(__name__)


class OrderService:
    """
    Service class for order operations.
    """
    
    @staticmethod
    def create_order_from_cart(user):
        """
        Create order from user's cart.
        """
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        
        if not cart_items.exists():
            raise ValueError("Корзина пуста")
        
        # Проверяем доступность товаров и баланс
        total_amount = Decimal('0.00')
        order_items_data = []
        
        for cart_item in cart_items:
            if not cart_item.can_be_ordered():
                raise ValueError(f"Товар {cart_item.product.name} недоступен для заказа")
            
            item_total = cart_item.total_price
            total_amount += item_total
            
            order_items_data.append({
                'product': cart_item.product,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
                'total_price': item_total
            })
        
        # Проверяем баланс пользователя
        if not user.has_sufficient_balance(total_amount):
            raise ValueError(f"Недостаточно средств на балансе. Требуется: {total_amount} руб.")
        
        try:
            with transaction.atomic():
                # Создаем заказ
                order = Order.objects.create(
                    user=user,
                    total_amount=total_amount,
                    status='pending'
                )
                
                # Создаем элементы заказа
                for item_data in order_items_data:
                    OrderItem.objects.create(
                        order=order,
                        **item_data
                    )
                
                # Списываем средства с баланса
                user.subtract_balance(total_amount)
                
                # Уменьшаем количество товаров на складе
                for cart_item in cart_items:
                    cart_item.product.decrease_stock(cart_item.quantity)
                
                # Очищаем корзину
                cart_items.delete()
                
                # Логируем успешный заказ
                logger.info(
                    f"Заказ #{order.id} успешно создан для пользователя {user.username}. "
                    f"Сумма: {total_amount} руб., товаров: {len(order_items_data)}"
                )
                
                return order
                
        except Exception as e:
            logger.error(f"Ошибка при создании заказа для пользователя {user.username}: {str(e)}")
            raise
    
    @staticmethod
    def cancel_order(order):
        """
        Cancel order and return items to stock.
        """
        if not order.can_be_cancelled():
            raise ValueError("Заказ не может быть отменен")
        
        try:
            with transaction.atomic():
                # Возвращаем товары на склад
                for item in order.order_items.all():
                    item.product.increase_stock(item.quantity)
                
                # Возвращаем деньги пользователю
                order.user.add_balance(order.total_amount)
                
                # Меняем статус заказа
                order.status = 'cancelled'
                order.save()
                
                # Логируем отмену заказа
                logger.info(
                    f"Заказ #{order.id} отменен для пользователя {order.user.username}. "
                    f"Возвращено: {order.total_amount} руб."
                )
                
                return order
                
        except Exception as e:
            logger.error(f"Ошибка при отмене заказа #{order.id}: {str(e)}")
            raise
    
    @staticmethod
    def get_order_summary(user):
        """
        Get order summary for user.
        """
        orders = Order.objects.filter(user=user).prefetch_related('order_items')
        
        total_orders = orders.count()
        total_spent = sum(order.total_amount for order in orders if order.status != 'cancelled')
        active_orders = orders.filter(status__in=['pending', 'paid', 'processing', 'shipped']).count()
        
        return {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'active_orders': active_orders
        }
    
    @staticmethod
    def validate_order_creation(user):
        """
        Validate if user can create order.
        """
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        
        if not cart_items.exists():
            return False, "Корзина пуста"
        
        total_amount = sum(item.total_price for item in cart_items)
        
        if not user.has_sufficient_balance(total_amount):
            return False, f"Недостаточно средств на балансе. Требуется: {total_amount} руб."
        
        for cart_item in cart_items:
            if not cart_item.can_be_ordered():
                return False, f"Товар {cart_item.product.name} недоступен для заказа"
        
        return True, "Заказ может быть создан" 