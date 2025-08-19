"""
Product models for the shop.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Product category model.
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model.
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Цена'
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def is_in_stock(self):
        """
        Check if product is in stock.
        """
        return self.stock_quantity > 0

    def has_sufficient_stock(self, quantity):
        """
        Check if product has sufficient stock.
        """
        return self.stock_quantity >= quantity

    def decrease_stock(self, quantity):
        """
        Decrease stock quantity.
        """
        if not self.has_sufficient_stock(quantity):
            raise ValueError(f"Недостаточно товара на складе. Доступно: {self.stock_quantity}")
        
        self.stock_quantity -= quantity
        self.save()

    def increase_stock(self, quantity):
        """
        Increase stock quantity.
        """
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        
        self.stock_quantity += quantity
        self.save() 