from rest_framework.filters import SearchFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.api.v1.serializers.serializer_user import UserSerializer, UserAlterPasswordSerializer
from main.models import User

PERMISSION_CLASSES = (IsAuthenticated,)


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter().all()
    permission_classes = PERMISSION_CLASSES
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('first_name', 'last_name', 'username', 'email')


class UserAlterPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAlterPasswordSerializer
    permission_classes = (AllowAny,)
