from django.contrib.admin.models import DELETION, CHANGE
from rest_framework import generics, filters, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from main.api.v1.serializers.serializers_brand import BrandSerializer, BrandCreateSerializer, \
    BrandRetrieveUpdateAPISerializer
from main.api.v1.utils import ActionsForLogEntry
from main.models import Brand

PERMISSION_CLASSES = (IsAuthenticated, IsAdminUser)


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class BrandCreateAPIView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandCreateSerializer
    permission_classes = PERMISSION_CLASSES


class BrandRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandRetrieveUpdateAPISerializer
    lookup_field = 'pk'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        log = ActionsForLogEntry()
        log.insert_log_entry(
            request,
            instance,
            {},
            CHANGE,
            self.serializer_class.__name__
        )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        log = ActionsForLogEntry()

        log.insert_log_entry(

            request, instance,

            {}, DELETION,

            self.serializer_class.__name__)

        return super().destroy(request, *args, **kwargs)
