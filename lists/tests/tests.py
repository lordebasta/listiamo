from datetime import datetime
import uuid
from django.test import TestCase
from lists.models import ListModel
from lists import list_repo


class ListRepoTestCase(TestCase):
    def setUp(self) -> None:
        listA = ListModel.objects.create(
            id="c9224235-d04d-4849-9ffd-b4226d5582f3",
            name="ListA",
            last_visited=datetime.today(),
        )
        listA.item_set.create(name="itemA1", link="https://www.google.com")

    def test_create_list(self):
        listB = list_repo.create_list("listB")
        self.assertTrue(ListModel.objects.filter(pk=listB.id).exists())
