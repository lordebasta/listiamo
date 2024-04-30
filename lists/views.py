from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .models import ListModel, Item

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


def delete_item(request, list_id):
    list = get_object_or_404(ListModel, pk=list_id)
    try:
        item = list.item_set.get(pk=request.POST["item"])
    except (KeyError, Item.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "list": list
            },
        )
    else:
        item.delete()
        return redirect('lists:detail', pk=list_id)

def create_item(request, list_id):
    list = get_object_or_404(ListModel, pk = list_id)
    
    item_name = request.POST["item_name"]
    item_link = request.POST["item_link"]

    if item_link and not item_link.startswith("https://") and not item_link.startswith("http://"):
        item_link = "//" + item_link

    item = Item(list=list, name=item_name, link=item_link)
    item.save()

    return redirect('lists:detail', pk=list_id)

def create_list(request):
    list_name = request.POST["list_name"]
    list = ListModel(name=list_name)
    list.save()

    return redirect('lists:detail', pk=list.id)