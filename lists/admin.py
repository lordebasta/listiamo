from django.contrib import admin
from .models import ListModel
from .models import Item

admin.site.register(ListModel)
admin.site.register(Item)