from django.conf import settings
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from . import list_repo
from .models import ListModel, Item


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "favicon.png").open("rb")
    return FileResponse(file)


def get_lists(request):
    lists = list_repo.get_lists()
    return render(request, "lists/index.html", {"lists_list": lists})


def get_list(request, pk):
    try:
        list = list_repo.get_list(pk)
    except ListModel.DoesNotExist:
        raise Http404(f"No list found with id {pk}")

    return render(request, "lists/detail.html", {"list": list})


def delete_item(request, list_id):
    item_id = request.POST["item"]
    try:
        list_repo.delete_item(list_id, item_id)
    except ListModel.DoesNotExist:
        return Http404(f"No list with id {list_id}")
    except (KeyError, Item.DoesNotExist):
        return render(
            request,
            "lists/detail.html",
            {
                "list": list
            },
        )
    return redirect('lists:detail', pk=list_id)


def create_item(request, list_id):
    item_name = request.POST["item_name"]
    item_link = request.POST["item_link"]

    try:
        list_repo.create_item(list_id, item_name, item_link)
    except ListModel.DoesNotExist:
        return Http404(f"No list with id {list_id}")

    return redirect('lists:detail', pk=list_id)


def create_list(request):
    list_name = request.POST["list_name"]
    list = list_repo.create_list(list_name)

    return redirect('lists:detail', pk=list.id)
