from django.contrib import admin
from .models import ListModel
from .models import Movie

admin.site.register(ListModel)
admin.site.register(Movie)