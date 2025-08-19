"""
Django management command to initialize test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.products.models import Category, Product
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    """Django command to initialize test data"""

    def handle(self, *args, **options):
        self.stdout.write('Initializing test data...')
        
        # Create test categories
        electronics, _ = Category.objects.get_or_create(
            name='Электроника',
            defaults={'description': 'Электронные устройства и гаджеты'}
        )
        
        books, _ = Category.objects.get_or_create(
            name='Книги',
            defaults={'description': 'Книги различных жанров'}
        )
        
        clothing, _ = Category.objects.get_or_create(
            name='Одежда',
            defaults={'description': 'Мужская и женская одежда'}
        )
        
        self.stdout.write('✅ Categories created')
        
        # Create test products
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Современный смартфон с отличной камерой',
                'price': Decimal('89999.99'),
                'stock_quantity': 50,
                'category': electronics
            },
            {
                'name': 'MacBook Air M2',
                'description': 'Легкий и мощный ноутбук',
                'price': Decimal('129999.99'),
                'stock_quantity': 25,
                'category': electronics
            },
            {
                'name': 'Война и мир',
                'description': 'Классический роман Льва Толстого',
                'price': Decimal('599.99'),
                'stock_quantity': 100,
                'category': books
            },
            {
                'name': 'Дюна',
                'description': 'Научно-фантастический роман Фрэнка Герберта',
                'price': Decimal('799.99'),
                'stock_quantity': 75,
                'category': books
            },
            {
                'name': 'Джинсы Levi\'s',
                'description': 'Классические джинсы премиум качества',
                'price': Decimal('3999.99'),
                'stock_quantity': 200,
                'category': clothing
            },
            {
                'name': 'Футболка Nike',
                'description': 'Спортивная футболка из дышащей ткани',
                'price': Decimal('1999.99'),
                'stock_quantity': 150,
                'category': clothing
            }
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
        
        self.stdout.write('✅ Products created')
        
        # Create test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )
        
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('✅ Test user created')
        else:
            self.stdout.write('ℹ️  Test user already exists')
        
        self.stdout.write(self.style.SUCCESS('✅ Test data initialization completed!'))
        self.stdout.write('👤 Test user: testuser / testpass123')
        self.stdout.write('👑 Admin user: admin / admin123') 