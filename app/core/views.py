"""
Core views for the project.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'message': 'Интернет-магазин API работает'
    }, status=status.HTTP_200_OK)


class HealthCheckView:
    """
    Health check view class.
    """
    @staticmethod
    def as_view():
        return health_check 