"""
Tests for users app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

User = get_user_model()


class UserModelTest(TestCase):
    """Test user model."""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.balance, Decimal('0.00'))

    def test_user_balance_operations(self):
        """Test user balance operations."""
        user = User.objects.create_user(**self.user_data)
        
        # Test adding balance
        user.add_balance(Decimal('100.00'))
        self.assertEqual(user.balance, Decimal('100.00'))
        
        # Test subtracting balance
        user.subtract_balance(Decimal('50.00'))
        self.assertEqual(user.balance, Decimal('50.00'))
        
        # Test insufficient balance
        with self.assertRaises(ValueError):
            user.subtract_balance(Decimal('100.00'))


class UserAPITest(APITestCase):
    """Test user API endpoints."""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """Test user registration."""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        """Test user login."""
        # Create user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_profile(self):
        """Test user profile endpoint."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_add_balance(self):
        """Test adding balance to user account."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=user)
        
        balance_data = {'amount': '100.00'}
        response = self.client.post('/api/auth/balance/', balance_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if balance was updated
        user.refresh_from_db()
        self.assertEqual(user.balance, Decimal('100.00')) 