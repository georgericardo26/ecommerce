from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import json

from main.api.v1.serializers.serializers_extra_product_type import ExtraProductTypeSerializer, \
    ExtraProductTypeSerializerResume
from main.api.v1.utils import ActionsForLogEntry
from main.models import Brand, LogSystem, Product, User


class ProductSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField()
    extra_product_type = ExtraProductTypeSerializerResume(many=True, read_only=True)
    pk_instance = None

    class Meta:
        model = Product
        fields = ('pk',
                  'code_name',
                  'name',
                  'description',
                  'price',
                  'created_by',
                  'extra_product_type',
                  'image',
                  'created_at',
                  'typeproduct',
                  'brand',)

    def get_created_by(self, obj):

        creator = None
        constraints = {
            "object_id": None,
            "action_flag": ADDITION,
            "object_repr": "ProductSerializer"
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


class ProductCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=1, max_length=50)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        instance_super = super(ProductCreateSerializer, self).create(validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, ADDITION, "ProductCreateSerializer")
        return instance_super


class ProductRetrieveUpdateAPISerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=1, max_length=50)

    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        instance_super = super(ProductRetrieveUpdateAPISerializer, self).update(instance, validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, CHANGE, "ProductRetrieveUpdateAPISerializer")
        return instance_super
