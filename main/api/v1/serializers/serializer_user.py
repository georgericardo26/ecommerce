from django.contrib.auth import password_validation
from rest_framework import serializers

from main.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get("password", None):
            instance.set_password(validated_data.get("password"))

        instance.save()

        return instance


class UserAlterPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        fields = '__all__'
        model = User

    def validate_password(self, data):
        password_validation.validate_password(password=data)
        return data

    def update(self, instance, validated_data):

        try:

            if User.objects.filter(username=instance).exists():
                user = User.objects.get(username=instance)
                user.set_password(validated_data["password"])
                user.save()
                return user

        except Exception:
            raise serializers.ErrorDetail({"Error": "Something wrong happend"})


