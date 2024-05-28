from rest_framework import serializers

from .models import Item, ListModel


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListModel
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['list']
