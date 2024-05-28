from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from lists import list_repo
from lists.models import Item, ListModel
from lists.serializers import ItemSerializer, ListSerializer


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

    @parser_classes((JSONParser,))
    def post(self, request):
        if not 'list_name' in request.data:
            return Response({'error':  'missing field \'list_name\' in body.'}, status=400)

        list_name = request.data['list_name']
        list = list_repo.create(list_name)

        items = list_repo.get_items(list.id)
        data = ListSerializer(list).data
        data['items'] = [ItemSerializer(item).data for item in items]
        return Response(data, status=201)


class ItemView(APIView):
    @parser_classes((JSONParser,))
    def post(self, request, list_id):
        if not 'item_name' in request.data:
            return Response({'error':  'missing field \'item_name\' in body.'}, status=400)
        item_name = request.data['item_name']
        item_link = request.data['item_link'] if 'item_link' in request.data else ''
        try:
            list_repo.create_item(list_id, item_name, item_link)
            return Response(status=201)
        except ListModel.DoesNotExist:
            return Response({'error': 'no list found'}, status=404)

    @parser_classes((JSONParser,))
    def delete(self, request, list_id):
        if not 'item_id' in request.data:
            return Response({'error': 'missing field \'item_id\' in body.'}, status=400)
        item_id = request.data['item_id']
        try:
            list_repo.delete_item(list_id, item_id)
        except ListModel.DoesNotExist:
            return Response({'error': 'no list found'}, status=404)
        except Item.DoesNotExist:
            return Response({'error': 'no item found'}, status=404)

        return Response(status=204)
