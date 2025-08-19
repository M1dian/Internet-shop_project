"""
Cart models for the shop.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from app.products.models import Product

User = get_user_model()


class CartItem(models.Model):
    """
    Cart item model.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['user', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        """
        Calculate total price for this item.
        """
        return self.product.price * self.quantity

    def update_quantity(self, new_quantity):
        """
        Update item quantity.
        """
        if new_quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        
        if not self.product.has_sufficient_stock(new_quantity):
            raise ValueError(f"Недостаточно товара на складе. Доступно: {self.product.stock_quantity}")
        
        self.quantity = new_quantity
        self.save()

    def can_be_ordered(self):
        """
        Check if item can be ordered.
        """
        return (
            self.product.is_active and
            self.product.has_sufficient_stock(self.quantity)
        ) 