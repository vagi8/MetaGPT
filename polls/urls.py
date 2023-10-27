from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^trigger_error', views.trigger_error, name='trigger_error'),
]
