import uuid
from django.db import models


class ListModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    last_visited = models.DateField()

    def __str__(self):
        return self.name

class Item(models.Model):
    list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name