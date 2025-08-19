"""
Order models for the shop.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from app.products.models import Product
from decimal import Decimal

User = get_user_model()


class Order(models.Model):
    """
    Order model.
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Общая сумма'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username} ({self.total_amount} руб.)"

    @property
    def items_count(self):
        """
        Get total items count in order.
        """
        return sum(item.quantity for item in self.order_items.all())

    def can_be_cancelled(self):
        """
        Check if order can be cancelled.
        """
        return self.status in ['pending', 'paid']

    def cancel_order(self):
        """
        Cancel order and return items to stock.
        """
        if not self.can_be_cancelled():
            raise ValueError("Заказ не может быть отменен")
        
        # Возвращаем товары на склад
        for item in self.order_items.all():
            item.product.increase_stock(item.quantity)
        
        # Возвращаем деньги пользователю
        self.user.add_balance(self.total_amount)
        
        self.status = 'cancelled'
        self.save()


class OrderItem(models.Model):
    """
    Order item model.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Цена за единицу'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Общая стоимость'
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.product.name} x{self.quantity} - {self.total_price} руб."

    def save(self, *args, **kwargs):
        """
        Calculate total price before saving.
        """
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs) 