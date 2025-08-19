"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin.
    """
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin.
    """
    list_display = [
        'name', 'category', 'price', 'stock_quantity',
        'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Цена и склад', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at'] 