"""
User models for the shop.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    """
    Custom user model with balance field.
    """
    email = models.EmailField(unique=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"

    def add_balance(self, amount):
        """
        Add amount to user balance.
        """
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        """
        Subtract amount from user balance.
        """
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if self.balance < amount:
            raise ValueError("Недостаточно средств на балансе")
        self.balance -= amount
        self.save()

    def has_sufficient_balance(self, amount):
        """
        Check if user has sufficient balance.
        """
        return self.balance >= amount 