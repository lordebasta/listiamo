from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from lists import list_repo
from lists.serializers import CreateItemSerializer, CreateListSerializer, DeleteItemSerializer
from lists.models import Item, ListModel
from lists.serializers import ItemSerializer, ListSerializer


class CreateListView(APIView):
    @parser_classes((JSONParser,))
    def post(self, request):

        serializer = CreateListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        list_name = serializer.data['name']

        list = list_repo.create_list(list_name)

        items = list_repo.get_items(list.id)
        data = ListSerializer(list).data
        data['items'] = [ItemSerializer(item).data for item in items]
        return Response(data, status=201)


class ListView(APIView):
    def get(self, request, list_id):
        try:
            list = list_repo.get_list(list_id)
        except ListModel.DoesNotExist:
            return Response({'error': 'no list found'}, status=404)

        items = list_repo.get_items(list_id)
        data = ListSerializer(list).data
        data['items'] = [ItemSerializer(item).data for item in items]
        return Response(data)


class ItemView(APIView):
    @parser_classes((JSONParser,))
    def post(self, request, list_id):
        serializer = CreateItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        item_name = serializer.data['name']
        item_link = serializer.data['link'] if 'link' in serializer.data else ''
        try:
            list_repo.create_item(list_id, item_name, item_link)
            return Response(status=201)
        except ListModel.DoesNotExist:
            return Response({'error': 'no list found'}, status=404)

    @parser_classes((JSONParser,))
    def delete(self, request, list_id):
        serializer = DeleteItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        item_id = serializer.data['id']
        try:
            list_repo.delete_item(list_id, item_id)
        except ListModel.DoesNotExist:
            return Response({'error': 'no list found'}, status=404)
        except Item.DoesNotExist:
            return Response({'error': 'no item found'}, status=404)

        return Response(status=204)
