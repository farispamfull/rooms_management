from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import UserSerializer

User = get_user_model()


class ReadOnlyOrDestroyViewSet(ReadOnlyModelViewSet, DestroyModelMixin):
    pass


class UserViewSet(ReadOnlyOrDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'phone']

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
