from datetime import date
import uuid
from .models import ListModel, Item
from django.db.models.query import QuerySet


def get_lists() -> QuerySet:
    return ListModel.objects.all()


def get_list(list_id: uuid.uuid4) -> ListModel:
    try:
        list = ListModel.objects.get(pk=list_id)
    except ListModel.DoesNotExist as e:
        raise e
    list.last_visited = date.today()
    list.save()
    return list


def create_list(list_name: str) -> ListModel:
    list = ListModel(name=list_name, last_visited=date.today())
    list.save()
    return list


def delete_item(list_id: uuid.uuid4, item_id: int) -> None:
    try:
        ListModel.objects.get(pk=list_id).item_set.get(pk=item_id).delete()
    except (ListModel.DoesNotExist, Item.DoesNotExist) as e:
        raise e


def create_item(list_id: uuid.uuid4, item_name: str, item_link: str) -> None:
    try:
        list = get_list(list_id)
    except ListModel.DoesNotExist as e:
        raise e
    if item_link and not item_link.startswith("https://") and not item_link.startswith("http://"):
        item_link = "//" + item_link
    item = Item(list=list, name=item_name, link=item_link)
    item.save()
