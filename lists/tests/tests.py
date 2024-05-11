from datetime import datetime
from django.test import TestCase
from lists.models import ListModel
from lists import list_repo


class ListRepoTestCase(TestCase):
    def setUp(self) -> None:
        listA = ListModel.objects.create(
            id="c9224235-d04d-4849-9ffd-b4226d5582f3",
            name="listA",
            last_visited=datetime(2024, 5, 11, 13, 3, 7, 8903),
        )
        listA.item_set.create(name="itemA1", link="https://www.google.com")

    def test_create_list(self):
        listB = list_repo.create_list("listB")
        self.assertTrue(ListModel.objects.filter(pk=listB.id).exists())

    def test_create_list_name_too_long(self):
        names = ["a" * 101, "a" * 200]
        for name in names:
            with self.subTest(msg=f"name length = {len(name)}"):
                self.assertRaises(ValueError, list_repo.create_list, name)

    def test_get_lists(self):
        ListModel.objects.create(
            id="c9224235-d04d-4849-9ffd-b4236d5582f3",
            name="listB",
            last_visited=datetime.now())
        lists = ListModel.objects.all()
        self.assertEqual(len(lists), 2)
        self.assertEqual(lists[0].name, "listA")
        self.assertEqual(lists[1].name, "listB")
