from django.contrib.admin.models import DELETION, CHANGE
from rest_framework import generics, filters, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from main.api.v1.mixins import MultipleFieldLookupMixin
from main.api.v1.serializers.serializers_brand import BrandSerializer, BrandCreateSerializer, \
    BrandRetrieveUpdateAPISerializer
from main.api.v1.serializers.serializers_extra_product_type import ExtraProductTypeSerializer, \
    ExtraProductTypeCreateSerializer, ExtraProductTypeRetrieveUpdateAPISerializer
from main.api.v1.utils import ActionsForLogEntry
from main.models import Brand, ExtraProductType

PERMISSION_CLASSES = (IsAuthenticated, IsAdminUser)


class ExtraProductTypeListAPIView(generics.ListAPIView):
    queryset = ExtraProductType.objects.all()
    serializer_class = ExtraProductTypeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'value',)


class ExtraProductTypeCreateAPIView(generics.CreateAPIView):
    queryset = ExtraProductType.objects.all()
    serializer_class = ExtraProductTypeCreateSerializer
    permission_classes = PERMISSION_CLASSES


class ExtraProductTypeRetrieveUpdateAPIView(MultipleFieldLookupMixin,
                                            generics.RetrieveUpdateDestroyAPIView):
    queryset = ExtraProductType.objects.all()
    serializer_class = ExtraProductTypeRetrieveUpdateAPISerializer
    lookup_fields = ('pk', 'name',)
    permission_classes = PERMISSION_CLASSES

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
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        log = ActionsForLogEntry()

        log.insert_log_entry(

            request, instance,

            {}, DELETION,

            self.serializer_class.__name__)

        return super().destroy(request, *args, **kwargs)
