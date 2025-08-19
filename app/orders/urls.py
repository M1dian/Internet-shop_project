"""
URL configuration for orders app.
"""
from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderCancelView,
    OrderStatusUpdateView,
    OrderSummaryView,
    OrderValidateView,
    AdminOrderListView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('validate/', OrderValidateView.as_view(), name='order-validate'),

    # Admin endpoints
    path('admin/list/', AdminOrderListView.as_view(), name='admin-order-list'),
]