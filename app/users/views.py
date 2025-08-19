"""
User views for the shop.
"""
from rest_framework import status, generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserBalanceSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration view.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Пользователь успешно зарегистрирован',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    User login view.
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Успешный вход',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserBalanceView(views.APIView):
    """
    User balance management view.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        user = request.user

        try:
            user.add_balance(amount)
            return Response({
                'message': f'Баланс пополнен на {amount} руб.',
                'new_balance': user.balance
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(views.APIView):
    """
    Get detailed user profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)