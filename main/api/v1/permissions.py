from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers

from main.models import User

from main.models import Client


class IsAdminProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.is_superuser


class IsClientProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request.user, 'client')


class IsUserOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    
    queryset = User.objects

    def has_permission(self, request, view):
        try:
            obj = self.queryset.get(**view.__dict__['kwargs'])
            return self.has_object_permission(request, view, obj)
        except Exception:
            pass

        return False

    def has_object_permission(self, request, view, obj):
        is_update_or_get = False
        if request.method in ['GET', 'PUT', 'PATCH']:
            is_update_or_get = True

        return (obj.pk == request.user.pk)


class IsClientOwner(IsUserOwner):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    queryset = Client.objects
