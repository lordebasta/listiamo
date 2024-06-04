from datetime import datetime
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from lists.models import Item, ListModel
from lists import list_repo
import json


class ApiTestCase(TestCase):
    def setUp(self) -> None:
        self.listA = ListModel.objects.create(
            id="c9224235-d04d-4849-9ffd-b4226d5582f3",
            name="listA",
            last_visited=datetime(2024, 5, 11, 13, 3, 7, 8903),
        )
        Item.objects.create(list=self.listA, name="itemA1",
                            link="https://www.google.com")
        self.listA = ListModel.objects.get(pk=self.listA.id)

    def test_create_list(self):
        c = Client()
        endpoint = "/api/list"
        with self.subTest(msg="correct creation"):
            response = c.post(endpoint, {"list_name": "listB"})
            self.assertEqual(response.status_code, 201)
            body = json.loads(response.content)
            self.assertEqual(body["name"], "listB")
            list_id = body['id']
            self.assertEqual("listB", ListModel.objects.get(pk=list_id).name)
        with self.subTest(msg="missing list name"):
            response = c.post(endpoint, {})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertTrue("error" in body)
            self.assertEqual(
                'missing field \'list_name\' in body.', body["error"])

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

    def test_create_item(self):
        list_id = self.listA.id

        with self.subTest(msg="item with name and link"):
            item_name = "item1"
            item_link = "google.com"
            list_repo.create_item(list_id, item_name, item_link)
            items = ListModel.objects.get(pk=list_id).item_set.all()
            self.assertEqual(len(items), 2)
            self.assertEqual(items[1].name, item_name)
            self.assertEqual(items[1].link, "//" + item_link)

        with self.subTest(msg="item with only name"):
            item_name = "item-with-no-link"
            list_repo.create_item(list_id, item_name)
            items = ListModel.objects.get(pk=list_id).item_set.all()
            item = items.get(name=item_name)
            self.assertEqual(len(items), 3)
            self.assertEqual(item.name, item_name)
            self.assertEqual(item.link, "")

    def test_create_item_exception(self):
        with self.subTest(msg="list_id not a uuid4"):
            self.assertRaisesRegex(
                ValidationError, "['“ciao” is not a valid UUID.']", list_repo.create_item, "ciao", "name", "link")

        with self.subTest(msg="no arguments provided"):
            self.assertRaisesRegex(
                TypeError, ".*missing 2 required positional.*", list_repo.create_item)

        with self.subTest(msg="no item name provided"):
            self.assertRaisesRegex(
                TypeError, ".*missing 1 required positional argument: 'item_name'.*", list_repo.create_item, self.listA.id)

        with self.subTest(msg="item name empty"):
            self.assertRaisesRegex(
                ValueError, "item_name can't be empty", list_repo.create_item, self.listA.id, "")

        with self.subTest(msg="item name too long"):
            self.assertRaisesRegex(
                ValueError, "The list name can be at max 100 characters long.", list_repo.create_item, self.listA.id, "a"*101)

        with self.subTest(msg="item link too long"):
            self.assertRaisesRegex(
                ValueError, "The list link can be at max 255 characters long.", list_repo.create_item, self.listA.id, "name", "a"*256)

    def test_delete_item(self):
        item_id = (self.listA.item_set.all())[0].id
        list_repo.delete_item(self.listA.id, item_id)
        self.assertEqual(len(ListModel.objects.get(
            pk=self.listA.id).item_set.all()), 0)

    def test_delete_item_error(self):
        with self.subTest(msg="List does not exists"):
            self.assertRaises(ListModel.DoesNotExist, list_repo.delete_item,
                              "9c89fccf-1943-4c1f-b8a3-87724c2ad762", 1)
        with self.subTest(msg="Item does not exists"):
            self.assertRaises(Item.DoesNotExist, list_repo.delete_item,
                              self.listA.id, 10)
