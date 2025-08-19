from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    # Добавляем поле 'balance' к стандартным fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Баланс', {'fields': ('balance',)}),
    )
    
    readonly_fields = ['created_at', 'updated_at']