from functools import reduce
import operator

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get
    multiple field filtering based on a `lookup_fields`
    attribute, instead of the default single field
    filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter[field] = self.kwargs[field]
        try:
            obj = None
            if 'user__email' in filter:
                exists = User.objects.filter(username=filter['user__email']).exists()
                if exists:
                    obj = User.objects.get(username=filter['user__email'])
            if not obj:
                obj = get_object_or_404(queryset, **filter)
        except MultipleObjectsReturned:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj


class MultipleFieldLookupMixinListAPIView(object):
    """
    Apply this mixin to any view or viewset to get
    multiple field filtering based on a `lookup_fields`
    attribute, instead of the default single field
    filtering.
    """

    def get_queryset(self):
        queryset = self.queryset          # Get the base queryset
        # queryset = self.filter_queryset(queryset)  # Apply any filter backends
        conditions = []
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):  # Ignore empty fields.
                for name in self.many_to_many_fields:
                    filter = {
                        '{}__in'.format(name): [self.kwargs[field]],
                    }
                    conditions.append(Q(**filter))

        #obj = get_object_or_404(queryset, reduce(operator.or_, conditions))
        #obj = get_object_or_404(queryset, **conditions)
        #self.check_object_permissions(self.request, obj)
        if conditions:
            return queryset.filter(reduce(operator.or_, conditions))
        return queryset.distinct()
