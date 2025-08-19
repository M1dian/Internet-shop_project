"""
Order views for the shop.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    OrderSummarySerializer
)
from .services import OrderService


class OrderListView(generics.ListAPIView):
    """
    User orders list view.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('order_items')


class OrderDetailView(generics.RetrieveAPIView):
    """
    Order detail view.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('order_items')


class OrderCreateView(generics.CreateAPIView):
    """
    Create order from cart view.
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = OrderService.create_order_from_cart(request.user)
            
            return Response({
                'message': 'Заказ успешно создан',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Произошла ошибка при создании заказа'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCancelView(generics.GenericAPIView):
    """
    Cancel order view.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        try:
            OrderService.cancel_order(order)
            
            return Response({
                'message': 'Заказ успешно отменен',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Произошла ошибка при отмене заказа'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderStatusUpdateView(generics.UpdateAPIView):
    """
    Update order status view (admin only).
    """
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_summary(request):
    """
    Get order summary for user.
    """
    summary = OrderService.get_order_summary(request.user)
    return Response(OrderSummarySerializer(summary).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_order(request):
    """
    Validate if order can be created.
    """
    try:
        can_create, message = OrderService.validate_order_creation(request.user)
        
        if can_create:
            return Response({
                'can_create': True,
                'message': message
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'can_create': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'can_create': False,
            'message': 'Произошла ошибка при проверке'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Admin views
class AdminOrderListView(generics.ListAPIView):
    """
    Admin order list view.
    """
    queryset = Order.objects.all().prefetch_related('order_items', 'user')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по статусу
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Фильтрация по пользователю
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset 