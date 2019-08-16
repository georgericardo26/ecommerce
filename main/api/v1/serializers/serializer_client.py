from django.contrib.admin.models import CHANGE
from django.contrib.auth import password_validation
from rest_framework import serializers

from main.api.v1.serializers.serializer_user import UserSerializer
from main.api.v1.utils import ActionsForLogEntry
from main.models import User, Client


class ClientSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    age_range = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(),
                                     validated_data=user_data)
        instance = Client()
        instance.user = user
        instance.cpf = validated_data.pop('cpf')
        instance.birthday = validated_data.pop('birthday')
        instance.gender = validated_data.pop('gender')
        instance.phone_number = validated_data.pop('phone_number')
        instance.save()

        return instance


class ClientRetrieveUpdateDestroySerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    age_range = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        user = instance.user
        if user_data:
            user = UserSerializer.update(UserSerializer(),
                                        instance=instance.user,
                                        validated_data=user_data)
        instance.user = user
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.save()

        log = ActionsForLogEntry()
        log.insert_log_entry(self.context['request'], instance,
                             validated_data, CHANGE, "ClientSerializer")

        return instance