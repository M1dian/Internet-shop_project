#!/usr/bin/env python
"""
Script to create a superuser for the shop.
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Create a superuser if it doesn't exist."""
    try:
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@shop.com',
                password='admin123'
            )
            print("✅ Суперпользователь создан успешно!")
            print("👤 Username: admin")
            print("🔑 Password: admin123")
            print("📧 Email: admin@shop.com")
        else:
            print("ℹ️  Суперпользователь уже существует")
    except Exception as e:
        print(f"❌ Ошибка при создании суперпользователя: {e}")

if __name__ == '__main__':
    create_superuser() 