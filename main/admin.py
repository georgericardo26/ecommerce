from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm)
from django import forms
from django.contrib.auth import get_user_model

from main.models import LogSystem, Client, Brand, ExtraProductType, ProductType, Product, Request

User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('deleted_in', 'is_deleted',)}),
    )


# class BrandAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'name']
#     list_filter = ('name',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(LogSystem)
admin.site.register(Client)
admin.site.register(Brand)
admin.site.register(ExtraProductType)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Request)


admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin API"
admin.site.index_title = "API Rest Ecommerce"