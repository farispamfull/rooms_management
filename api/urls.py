from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication.views import (UserRegistrationView, UserLoginView)
from users.views import UserViewSet
from .views import BookingViewSet, RoomViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('booking', BookingViewSet, basename='booking')
router_v1.register('rooms', RoomViewSet, basename='room')

auth_patterns = [path('signup/', UserRegistrationView.as_view()),
                 path('token/login/', UserLoginView.as_view()),
                 ]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
