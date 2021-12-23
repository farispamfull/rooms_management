from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .utils import login_user
from rest_framework import status
User = get_user_model()


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    # def perform_create(self, serializer):
    #     user = serializer.save()


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = login_user(request, serializer.validated_data('user'))
        return Response({'token': token.key}, status=status.HTTP_200_OK)
