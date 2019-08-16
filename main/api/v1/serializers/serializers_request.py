from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import json
from main.api.v1.utils import ActionsForLogEntry
from main.api.v1.validators import check_product_exists, check_client_exists, check_processor_qt, check_motherboard_qt, \
    check_motherboard_brand_processor
from main.models import Brand, LogSystem, ExtraProductType, Request

from main.api.v1.validators import check_memory_qt

from main.api.v1.validators import check_videoboard

from main.models import Client

from main.models import User


class RequestAPISerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    pk_instance = None

    class Meta:
        model = Request
        fields = ('id', 'total', 'products', 'date', 'client', 'url', 'created_at')
        extra_kwargs = {
            'url': {
                'view_name': 'v1:request_retrieve_update_destroy_by_pk',
                'lookup_field': 'pk',
            }
        }

    def update(self, instance, validated_data):
        instance_super = super(RequestAPISerializer, self).update(instance, validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, CHANGE, "RequestAPISerializer")
        return instance_super

    def get_created_by(self, obj):

        creator = None
        constraints = {
            "object_id": None,
            "action_flag": ADDITION,
            "object_repr": "RequestAPISerializer"
        }
        if self.pk_instance is None:
            constraints["object_id"] = str(obj.pk)
        else:
            constraints["object_id"] = str(self.pk_instance)

        log = LogSystem.objects.filter(**constraints).first()
        user_id = getattr(log, 'user_id', None)
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            creator = user.username

        return creator

    def get_total(self, obj):
        result = sum(obj.products.values_list("price", flat=True))
        return result

    def get_date(self, obj):
        return obj.created_at

    def get_products(self, obj):

        result = []
        queryset = obj.products.values("pk", "description", "brand_id", "price")
        return queryset


class RequestValidatorList(serializers.ListField):
    child = serializers.IntegerField(min_value=1, max_value=1000)


class RequestCreateSerializer(serializers.ModelSerializer):

    products = serializers.ListField()

    class Meta:
        model = Request
        fields = '__all__'
        validators = (
                      check_product_exists,
                      check_processor_qt,
                      check_motherboard_qt,
                      check_motherboard_brand_processor,
                      check_memory_qt,
                      check_videoboard,
                      )

    def create(self, validated_data):

        obj = {"products": []}
        for pk in validated_data["products"]:
            obj["products"].append(int(pk["id"]))
        obj["client"] = Client.objects.get(pk=self.context['request'].user.pk)
        instance_super = super(RequestCreateSerializer, self).create(obj)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                                 validated_data, ADDITION, "RequestCreateSerializer")
        return validated_data

    def update(self, instance, validated_data):

        obj = {"products": []}
        for pk in validated_data["products"]:
            obj["products"].append(int(pk["id"]))
        obj["client"] = Client.objects.get(pk=self.context['request'].user.pk)
        instance_super = super(RequestCreateSerializer, self).update(instance, obj)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                                 validated_data, CHANGE, "RequestCreateSerializer")
        return validated_data