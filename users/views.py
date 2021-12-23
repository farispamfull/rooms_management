from django.contrib.auth import get_user_model
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

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        # serializer = self.get_serializer(request.user, data=request.data,
        #                                  partial=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(email=request.user.email,
        #                 username=request.user.username)
        # return Response(serializer.data)