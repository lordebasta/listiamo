from django.urls import path

from . import views, api_views

app_name = "lists"
urlpatterns = [
    path("favicon.ico", views.favicon),
    path("", views.get_homepage, name="index"),
    path("<uuid:pk>/", views.get_list, name="detail"),
    path("<uuid:list_id>/del", views.delete_item, name="delete_item"),
    path("<uuid:list_id>/create", views.create_item, name="create_item"),
    path("create", views.create_list, name="create_list"),
    path("api/list", api_views.CreateListView.as_view()),
    path("api/<uuid:list_id>", api_views.ListView.as_view()),
    path("api/<uuid:list_id>/items", api_views.ItemView.as_view()),
]
