from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<uuid:pk>/", views.get_list, name="detail"),
    path("<uuid:list_id>/del", views.delete_item, name="delete_item"),
    path("<uuid:list_id>/create", views.create_item, name="create_item"),
    path("create", views.create_list, name="create_list")
]
