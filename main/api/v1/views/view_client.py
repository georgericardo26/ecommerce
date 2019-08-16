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

from main.api.v1.mixins import MultipleFieldLookupMixin
from main.api.v1.serializers.serializer_client import ClientSerializer, ClientRetrieveUpdateDestroySerializer
from main.api.v1.serializers.serializer_user import UserSerializer, UserAlterPasswordSerializer
from main.models import User, Client

PERMISSION_CLASSES = (IsAuthenticated, IsAdminUser)


class ClientListAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = PERMISSION_CLASSES
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('first_name', 'last_name', 'username', 'email')


class ClientCreateAPIView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (AllowAny,)


class ClientRetrieveUpdateDestroyAPIView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientRetrieveUpdateDestroySerializer
    queryset = Client.objects.all()
    permission_classes = PERMISSION_CLASSES
    lookup_fields = ('pk', 'user__username',)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(ClientRetrieveUpdateDestroyAPIView, self).get_serializer(*args, **kwargs)