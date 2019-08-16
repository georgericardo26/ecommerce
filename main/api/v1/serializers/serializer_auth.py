from django.contrib.admin.models import ADDITION

from main.api.v1.utils import ActionsForLogEntry
from main.models import User
from rest_framework import (serializers, pagination)


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
        }
    #
    # def create(self, validated_data):
    #
    #     instance_super = super(AuthSerializer, self).create(validated_data)
    #     log = ActionsForLogEntry()
    #     log.insert_log_entry(self.context['request'], instance_super,
    #                          validated_data, ADDITION, "AuthSerializer")
    #     return validated_data