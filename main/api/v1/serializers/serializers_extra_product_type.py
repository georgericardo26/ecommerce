from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import json
from main.api.v1.utils import ActionsForLogEntry
from main.models import Brand, LogSystem, ExtraProductType

User = get_user_model()


class ExtraProductTypeSerializerResume(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    value_type = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ExtraProductType
        fields = ('name', 'value_type', 'description',)

    def get_name(self, obj):
        return obj.name

    def get_value_type(self, obj):
        return obj.value

    def get_description(self, obj):
        return obj.description


class ExtraProductTypeSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField()
    pk_instance = None

    class Meta:
        model = ExtraProductType
        fields = '__all__'

    def get_created_by(self, obj):

        creator = None
        constraints = {
            "object_id": None,
            "action_flag": ADDITION,
            "object_repr": "ExtraProductTypeSerializer"
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


class ExtraProductTypeCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=1, max_length=50)
    value = serializers.CharField(min_length=1, max_length=100)

    class Meta:
        model = ExtraProductType
        fields = '__all__'

    def create(self, validated_data):
        instance_super = super(ExtraProductTypeCreateSerializer, self).create(validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, ADDITION, "ExtraProductTypeCreateSerializer")
        return instance_super


class ExtraProductTypeRetrieveUpdateAPISerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=1, max_length=50)
    value = serializers.CharField(min_length=1, max_length=100)

    class Meta:
        model = ExtraProductType
        fields = '__all__'

    def update(self, instance, validated_data):
        instance_super = super(ExtraProductTypeRetrieveUpdateAPISerializer, self).update(instance, validated_data)
        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance_super,
                             validated_data, CHANGE, "ExtraProductTypeRetrieveUpdateAPISerializer")
        return instance_super


