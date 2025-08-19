"""
Order views for the shop.
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
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


class OrderCreateView(APIView):
    """
    Create order from cart view.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderService.create_order_from_cart(request.user)
            return Response({
                'message': 'Заказ успешно создан',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Произошла ошибка при создании заказа'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCancelView(APIView):
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
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Произошла ошибка при отмене заказа'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderStatusUpdateView(generics.UpdateAPIView):
    """
    Update order status view (admin only).
    """
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]


class OrderSummaryView(APIView):
    """
    Get order summary for user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = OrderService.get_order_summary(request.user)
        return Response(OrderSummarySerializer(summary).data)


class OrderValidateView(APIView):
    """
    Validate if order can be created.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            can_create, message = OrderService.validate_order_creation(request.user)
            status_code = status.HTTP_200_OK if can_create else status.HTTP_400_BAD_REQUEST
            return Response({'can_create': can_create, 'message': message}, status=status_code)
        except Exception:
            return Response({'can_create': False, 'message': 'Произошла ошибка при проверке'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminOrderListView(generics.ListAPIView):
    """
    Admin order list view.
    """
    queryset = Order.objects.all().prefetch_related('order_items', 'user')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset