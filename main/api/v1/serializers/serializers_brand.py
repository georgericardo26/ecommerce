from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import json
from main.api.v1.utils import ActionsForLogEntry
from main.models import Brand, LogSystem

User = get_user_model()


class BrandSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField()
    pk_instance = None

    class Meta:
        model = Brand
        fields = '__all__'

    def get_created_by(self, obj):

        creator = None
        constraints = {
            "object_id": None,
            "action_flag": ADDITION,
            "object_repr": "BrandCreateSerializer"
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


class BrandCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=1, max_length=50)

    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        instance_super = super(BrandCreateSerializer, self).create(validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, ADDITION, "BrandCreateSerializer")
        return instance_super


class BrandRetrieveUpdateAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'

    def update(self, instance, validated_data):
        instance_super = super(BrandRetrieveUpdateAPISerializer, self).update(instance, validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, CHANGE, "BrandRetrieveUpdateAPISerializer")
        return instance_super
