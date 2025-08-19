"""
Admin configuration for cart app.
"""
from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Cart item admin.
    """
    list_display = ['user', 'product', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'product__name']
    ordering = ['-added_at']
    
    readonly_fields = ['added_at', 'updated_at']
    
    def total_price(self, obj):
        return f"{obj.total_price} руб."
    total_price.short_description = 'Общая стоимость' 