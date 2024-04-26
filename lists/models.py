from django.db import models


class ListModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.CharField()

    def __str__(self):
        return self.name