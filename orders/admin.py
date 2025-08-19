"""
Admin configuration for orders app.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Order admin.
    """
    list_display = [
        'id', 'user', 'status', 'total_amount',
        'items_count', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']
    
    inlines = [OrderItemInline]
    
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def items_count(self, obj):
        return obj.items_count
    items_count.short_description = 'Количество товаров'