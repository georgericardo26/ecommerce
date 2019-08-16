from django.contrib.admin.models import DELETION, CHANGE
from rest_framework import generics, filters, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from main.api.v1.filters import RequestListAPIFilter, RequestAPICheckClientFilterMark
from main.api.v1.serializers.serializers_extra_product_type import ExtraProductTypeSerializer, \
    ExtraProductTypeCreateSerializer, ExtraProductTypeRetrieveUpdateAPISerializer
from main.api.v1.serializers.serializers_request import RequestAPISerializer, RequestCreateSerializer
from main.api.v1.utils import ActionsForLogEntry
from main.models import Request

from main.api.v1.permissions import IsClientProfilePermission

PERMISSION_CLASSES = (IsAuthenticated,)


class RequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestAPISerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, RequestAPICheckClientFilterMark)
    filter_class = RequestListAPIFilter


class RequestCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
    permission_classes = (IsClientProfilePermission,)


class RequestRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestAPISerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated, IsAdminUser)

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
