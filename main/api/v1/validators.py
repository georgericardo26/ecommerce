import json
import string
import re
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (Permission, Group)
from django.db.models import Q
from rest_framework import serializers

from main.models import Product, Client


def check_product_exists(value):

    errors = []

    if value["products"]:
        for pk in value["products"]:
            if not Product.objects.filter(pk=pk["id"]).exists():
                errors.append(
                        {"error": 'Id %d is not a valid product.' % (pk["id"])}
                )

        if errors:
            raise serializers.ValidationError(errors)
    else:
        raise serializers.ValidationError({"error": "This product list can't be empty"})


def check_client_exists(value):
    if not Client.objects.filter(pk=value["client"]).exists():
        raise serializers.ValidationError(
            {"error": 'Id %d is not a valid client.' % (value["client"])})


def check_processor_qt(value):
    items = []
    qt_items = []

    for pk in value["products"]:
        product = Product.objects.get(pk=pk["id"])
        if product.typeproduct.pk is 1:
            items.append(product.typeproduct.pk)

    if items:
        if items.count(1) > 1:
            raise serializers.ValidationError(
                {"error": "You can't choose a quantity greater than 1 for this product"})
    if not items:
        raise serializers.ValidationError(
            {"error": "You need choose at least 1 product this type"})


def check_motherboard_qt(value):
    items = []
    qt_items = []

    for pk in value["products"]:
        product = Product.objects.get(pk=pk["id"])
        if product.typeproduct.pk is 2:
            items.append(product.typeproduct.pk)

    if items:
        if items.count(2) > 1:
            raise serializers.ValidationError(
                {"error": "You can't choose a quantity greater than 1 for this product"})

    if not items:
        raise serializers.ValidationError(
            {"error": "You need choose at least 1 product this type"})


def check_motherboard_brand_processor(value):
    obj = {}
    compatible = False

    for pk in value["products"]:
        product = Product.objects.get(pk=pk["id"])
        if product.typeproduct.pk is 2:
            obj["motherboard"] = product
        if product.typeproduct.pk is 1:
            obj["processor"] = product.brand

    values = obj["motherboard"].extra_product_type.values_list()
    for type in values:
        if str(obj["processor"]) in str(type):
            compatible = True

    if not compatible:
        raise serializers.ValidationError(
            {"error": "Motherboard and processor not be compatibles"})


def check_memory_qt(value):
    items = []
    extra_type = {}

    for pk in value["products"]:
        product = Product.objects.get(pk=pk["id"])
        if product.typeproduct.pk is 4:
            obj = next(item for item in product.extra_product_type.values() if item["name"] == "tamanho_memoria")
            items.append(int(re.search(r'\d+', obj["value"]).group()))

        if product.typeproduct.pk is 2:
            slot = next(item for item in product.extra_product_type.values() if item["name"] == "qtde_slots_memória_ram")
            capacity = next(item for item in product.extra_product_type.values() if item["name"] == "total_memoria_ram_suportado")

            extra_type["slots"] = int(re.search(r'\d+', slot["value"]).group())
            extra_type["capacity"] = int(re.search(r'\d+', capacity["value"]).group())

    if len(items) > extra_type["slots"]:
        raise serializers.ValidationError(
            {"error": "Quantity of memory is greater to motherboard slots"})

    if sum(items) > extra_type["capacity"]:
        raise serializers.ValidationError(
            {"error": "Quantity of memory is greater to motherboard capacity"})


def check_videoboard(value):
    items = []
    extra_type = {}

    for pk in value["products"]:
        product = Product.objects.get(pk=pk["id"])
        if product.typeproduct.pk is 3:
            items.append(product)

        if product.typeproduct.pk is 2:
            video_embed = next(item for item in product.extra_product_type.values() if item["name"] == "video_integrado")
            extra_type["video_embed"] = video_embed["value"]

    if len(items) == 0 and "Não" in str(extra_type["video_embed"]):
        raise serializers.ValidationError(
            {"error": "You need choose a videoboard for this motherboard"})

    if len(items) > 1:
        raise serializers.ValidationError(
            {"error": "You can choose only 1 videoboard for this motherboard"})

