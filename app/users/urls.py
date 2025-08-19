"""
URL configuration for users app.
"""
from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserBalanceView,
    UserProfileDetailView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/detail/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('balance/', UserBalanceView.as_view(), name='user-balance'),
]