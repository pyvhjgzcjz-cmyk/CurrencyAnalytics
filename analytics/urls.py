from django.urls import path
from . import views

urlpatterns = [
    path('', views.currency_analytics, name='currency_analytics'),
]