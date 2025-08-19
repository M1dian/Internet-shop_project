"""
URL configuration for cart app.
"""
from django.urls import path
from .views import (
    CartListView,
    CartItemAddView,
    CartItemUpdateView,
    CartItemRemoveView,
    CartSummaryView,
    ClearCartView,
    UpdateCartItemQuantityView
)

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),
    path('add/', CartItemAddView.as_view(), name='cart-add'),
    path('summary/', CartSummaryView.as_view(), name='cart-summary'),
    path('clear/', ClearCartView.as_view(), name='cart-clear'),
    path('<int:pk>/update/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('<int:pk>/remove/', CartItemRemoveView.as_view(), name='cart-item-remove'),
    path('<int:pk>/quantity/', UpdateCartItemQuantityView.as_view(), name='cart-item-quantity'),
]