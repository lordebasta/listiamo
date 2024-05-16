from datetime import date
import uuid
from .models import ListModel, Item
from django.db.models.query import QuerySet


def get_lists() -> QuerySet:
    return ListModel.objects.all()


def get_list(list_id: uuid.uuid4) -> ListModel:
    list = ListModel.objects.get(pk=list_id)
    list.last_visited = date.today()
    list.save()
    return list


def create_list(list_name: str) -> ListModel:
    if len(list_name) > 100:
        raise ValueError("The list name can be at max 100 characters long.")
    list: ListModel = ListModel(name=list_name, last_visited=date.today())
    list.save()
    return list


def create_item(list_id: uuid.uuid4, item_name: str, item_link: str = "") -> None:
    if item_name == "":
        raise ValueError("item_name can't be empty")
    if len(item_name) > 100:
        raise ValueError("The list name can be at max 100 characters long.")
    if len(item_link) > 255:
        raise ValueError("The list link can be at max 255 characters long.")

    list = get_list(list_id)
    if item_link and not item_link.startswith("https://") and not item_link.startswith("http://"):
        item_link = "//" + item_link
    item = Item(list=list, name=item_name, link=item_link)
    item.save()


def delete_item(list_id: uuid.uuid4, item_id: int) -> None:
    list_obj = get_list(list_id)
    list_obj.item_set.get(pk=item_id).delete()
