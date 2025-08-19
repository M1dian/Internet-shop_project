#!/usr/bin/env python
"""
Script to check project readiness.
"""
import os
import sys
import django
from pathlib import Path

def check_project():
    """Check if project is ready to run."""
    print("🔍 Проверка готовности проекта...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("❌ Требуется Python 3.11+")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check required files
    required_files = [
        'manage.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'README.md',
        'config/settings.py',
        'config/urls.py',
        'app/users/models.py',
        'app/products/models.py',
        'app/cart/models.py',
        'app/orders/models.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Отсутствуют файлы:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ Все необходимые файлы присутствуют")
    
    # Check Django setup
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        print("✅ Django настроен корректно")
    except Exception as e:
        print(f"❌ Ошибка настройки Django: {e}")
        return False
    
    # Check models
    try:
        from app.users.models import User
        from app.products.models import Product, Category
        from app.cart.models import CartItem
        from app.orders.models import Order, OrderItem
        print("✅ Все модели импортированы успешно")
    except Exception as e:
        print(f"❌ Ошибка импорта моделей: {e}")
        return False
    
    # Check URLs
    try:
        from config.urls import urlpatterns
        print("✅ URL конфигурация корректна")
    except Exception as e:
        print(f"❌ Ошибка URL конфигурации: {e}")
        return False
    
    print("\n🎉 Проект готов к запуску!")
    print("\n📋 Следующие шаги:")
    print("1. docker-compose up --build")
    print("2. docker-compose exec web python manage.py migrate")
    print("3. docker-compose exec web python manage.py init_data")
    print("4. Откройте http://localhost:8000/api/")
    
    return True

if __name__ == '__main__':
    check_project() 