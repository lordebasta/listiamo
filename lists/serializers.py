from rest_framework import serializers

from .models import Item, ListModel
from lists import models


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['list']


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        fields = ["name"]


class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "link"]


class DeleteItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
