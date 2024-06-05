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
            response = c.post(endpoint, {"name": "listB"})
            self.assertEqual(response.status_code, 201)
            body = json.loads(response.content)
            self.assertEqual(body["name"], "listB")
            list_id = body['id']
            self.assertEqual("listB", ListModel.objects.get(pk=list_id).name)
        with self.subTest(msg="missing list name"):
            response = c.post(endpoint, {})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                ['This field is required.'], body["name"])
        with self.subTest(msg="list name too long"):
            names = ["a" * 101, "a" * 200]
            for name in names:
                response = c.post(endpoint, {'name': name})
                body = json.loads(response.content)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    body['name'], ["Ensure this field has no more than 100 characters."])

    def test_create_item(self):
        list_id = self.listA.id
        endpoint = f"/api/{list_id}/items"
        c = Client()
        with self.subTest(msg="item with name and link"):
            item_name = "item1"
            item_link = "google.com"
            response = c.post(endpoint, {"name": item_name, "link": item_link})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content, b"")
            items = ListModel.objects.get(pk=list_id).item_set.all()
            self.assertEqual(len(items), 2)
            self.assertEqual(items[1].name, item_name)
            self.assertEqual(items[1].link, "//" + item_link)

        with self.subTest(msg="item with only name"):
            item_name = "item-with-no-link"
            response = c.post(endpoint, {"name": item_name})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content, b"")
            items = ListModel.objects.get(pk=list_id).item_set.all()
            item = items.get(name=item_name)
            self.assertEqual(len(items), 3)
            self.assertEqual(item.name, item_name)
            self.assertEqual(item.link, "")

    def test_create_item_exception(self):
        endpoint = f"/api/{self.listA.id}/items"
        c = Client()

        with self.subTest(msg="list_id not a uuid4"):
            response = c.post('/api/ciao/items',
                              {"name": "name", "link": "link"})
            self.assertEqual(response.status_code, 404)
            self.assertTrue(
                'The requested resource was not found on this server.' in str(response.content))

        with self.subTest(msg="no item name provided"):
            response = c.post(endpoint,  {})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(body['name'], ['This field is required.'])

        with self.subTest(msg="item name empty"):
            response = c.post(endpoint,  {'name': ''})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(body['name'], ['This field may not be blank.'])

        with self.subTest(msg="item name too long"):
            response = c.post(endpoint,  {'name': 'a'*101})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                body['name'], ["Ensure this field has no more than 100 characters."])

        with self.subTest(msg="item link too long"):
            response = c.post(endpoint,  {'name': 'name', "link": 'a'*256})
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                body['link'], ["Ensure this field has no more than 255 characters."])

    def test_delete_item(self):
        endpoint = f"/api/{self.listA.id}/items"
        c = Client()
        item_id = (self.listA.item_set.all())[0].id
        response = c.delete(
            endpoint, {"id": item_id}, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(len(ListModel.objects.get(
            pk=self.listA.id).item_set.all()), 0)

    def test_delete_item_error(self):
        c = Client()
        with self.subTest(msg="List does not exists"):
            response = c.delete(
                "/api/9c89fccf-1943-4c1f-b8a3-87724c2ad762/items", {"id": 8}, content_type='application/json')
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(body['error'], "no list found")
        with self.subTest(msg="Item does not exists"):
            response = c.delete(
                f"/api/{self.listA.id}/items", {"id": 9}, content_type='application/json')
            body = json.loads(response.content)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(body['error'], "no item found")
