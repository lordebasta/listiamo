from .models import ListModel
from datetime import timedelta, datetime


def delete_obsolete_lists():
    time_threshold = datetime.now() - timedelta(days=30)
    to_delete = ListModel.objects.filter(last_visited__lte=time_threshold)
    if to_delete:
        to_delete.delete()
