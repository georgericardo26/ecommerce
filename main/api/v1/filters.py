import django_filters
from django.contrib.auth import get_user_model

from main.models import Request, Product
from rest_framework import filters as rest_filters
from rest_framework import serializers


from main.models import Client


User = get_user_model()


class RequestAPICheckClientFilterMark(rest_filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_client = hasattr(request.user, 'client')

        if is_client:
            return queryset.filter(client__iexact=request.user.pk)

        return queryset


class RequestListAPIFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(method='get_client')
    client_username = django_filters.CharFilter(method='get_client_username')
    # created_at = django_filters.DateFromToRangeFilter(method='get_created_at')
    # price__gti = django_filters.CharFilter(method='get_price_gti')

    class Meta:
        model = Request
        fields = {
            'created_at': ['exact', 'range'],
        }

    def get_client(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

    def get_client_username(self, queryset, name, value):

        return queryset.filter(**{
            'client__user__username': value,
        })
    #
    # def get_created_at(self, queryset, name, value):
    #     return queryset.filter(created_at__range=value)


    # def get_price_gti(self, queryset, name, value):
    #
    #     items = []
    #     for price in queryset:
    #         # list_price = price.products.values("price")
    #         # list_price = [float(number) for number in list_price]
    #
    #         # if float(value) >= sum(list_price):
    #         items.append(price)
    #
    #     # raise serializers.ValidationError(items)
    #
    #     #     if float(value) >= sum(list_price):
    #     #         items.append(price)
    #     #
    #     return items


class ProductListAPIFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(method='get_description')

    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'range'],
            'created_at': ['exact', 'range']
        }

    def get_description(self, queryset, name, value):
        return queryset.filter(**{
            'description__icontains': value
        })