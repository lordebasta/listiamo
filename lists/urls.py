from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<uuid:pk>/", views.DetailView.as_view(), name="detail"),
    path("<uuid:list_id>/del", views.delete_movie, name="delete_movie"),
    path("<uuid:list_id>/create", views.create_movie, name="create_movie"),
    path("create", views.create_list, name="create_list")
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]