from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.config, name='stripe-config'),
    path('callback/', views.callback, name='stripe-callback')]
