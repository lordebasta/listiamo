from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .models import ListModel, Movie

class IndexView(generic.ListView):
    template_name = "lists/index.html"
    context_object_name = "lists_list"

    def get_queryset(self) -> QuerySet[Any]:
        return ListModel.objects.all();


# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = ListModel
    context_object_name = "list"
    template_name = "lists/detail.html"


def delete_movie(request, list_id):
    list = get_object_or_404(ListModel, pk=list_id)
    try:
        movie = list.movie_set.get(pk=request.POST["movie"])
    except (KeyError, Movie.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "list": list
            },
        )
    else:
        movie.delete()
        return redirect('lists:detail', pk=list_id)

def create_movie(request, list_id):
    list = get_object_or_404(ListModel, pk = list_id)
    
    movie_name = request.POST["movie_name"]
    movie_link = request.POST["movie_link"]
    movie = Movie(list=list, name=movie_name, link=movie_link)
    movie.save()

    return redirect('lists:detail', pk=list_id)

def create_list(request):
    list_name = request.POST["list_name"]
    list = ListModel(name=list_name)
    list.save()

    return redirect('lists:detail', pk=list.id)