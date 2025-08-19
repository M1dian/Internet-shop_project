"""
Cart views for the shop.
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CartItem
from .serializers import (
    CartItemSerializer,
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CartSummarySerializer
)


class CartListView(generics.ListAPIView):
    """
    Cart items list view.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product', 'product__category')


class CartItemAddView(generics.CreateAPIView):
    """
    Add item to cart view.
    """
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()


class CartItemUpdateView(generics.UpdateAPIView):
    """
    Update cart item quantity view.
    """
    serializer_class = CartItemUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class CartItemRemoveView(generics.DestroyAPIView):
    """
    Remove item from cart view.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_200_OK)


class CartSummaryView(APIView):
    """
    Get cart summary.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.total_price for item in cart_items)

        data = {
            'total_items': total_items,
            'total_price': total_price,
            'items': CartItemSerializer(cart_items, many=True).data
        }

        return Response(CartSummarySerializer(data).data)


class ClearCartView(APIView):
    """
    Clear all items from cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_200_OK)


class UpdateCartItemQuantityView(APIView):
    """
    Update cart item quantity.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)

        try:
            new_quantity = int(request.data.get('quantity', 1))
            cart_item.update_quantity(new_quantity)
            return Response({
                'message': 'Количество обновлено',
                'cart_item': CartItemSerializer(cart_item).data
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)