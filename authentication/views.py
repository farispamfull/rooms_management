from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .utils import login_user, logout_user

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = login_user(request, user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout_user(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
