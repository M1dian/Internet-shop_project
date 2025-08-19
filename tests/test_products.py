"""
Tests for products app.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from app.products.models import Category, Product
from app.users.models import User


class ProductModelTest(TestCase):
    """Test product model."""

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            stock_quantity=10,
            category=self.category
        )

    def test_product_creation(self):
        """Test product creation."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.stock_quantity, 10)

    def test_product_stock_operations(self):
        """Test product stock operations."""
        # Test decrease stock
        self.product.decrease_stock(5)
        self.assertEqual(self.product.stock_quantity, 5)
        
        # Test increase stock
        self.product.increase_stock(3)
        self.assertEqual(self.product.stock_quantity, 8)
        
        # Test insufficient stock
        with self.assertRaises(ValueError):
            self.product.decrease_stock(10)

    def test_product_in_stock(self):
        """Test product in stock check."""
        self.assertTrue(self.product.is_in_stock())
        
        self.product.stock_quantity = 0
        self.assertFalse(self.product.is_in_stock())


class ProductAPITest(APITestCase):
    """Test product API endpoints."""

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            stock_quantity=10,
            category=self.category
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

    def test_product_list(self):
        """Test product list endpoint."""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_detail(self):
        """Test product detail endpoint."""
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_product_create_admin_only(self):
        """Test product create endpoint (admin only)."""
        # Test without authentication
        product_data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '149.99',
            'stock_quantity': 5,
            'category': self.category.id
        }
        
        response = self.client.post('/api/products/create/', product_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with admin authentication
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/products/create/', product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_filtering(self):
        """Test product filtering."""
        # Create another product
        Product.objects.create(
            name='Cheap Product',
            description='Cheap Description',
            price=Decimal('19.99'),
            stock_quantity=5,
            category=self.category
        )
        
        # Test price filtering
        response = self.client.get('/api/products/?min_price=50')
        self.assertEqual(len(response.data['results']), 1)
        
        response = self.client.get('/api/products/?max_price=50')
        self.assertEqual(len(response.data['results']), 1)

    def test_category_list(self):
        """Test category list endpoint."""
        response = self.client.get('/api/products/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 