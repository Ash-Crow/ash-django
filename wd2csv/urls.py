from django.conf.urls import url
from wd2csv import views as wd2csv_views

urlpatterns = [
    url(r'', wd2csv_views.index),
]