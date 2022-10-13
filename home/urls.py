from django.urls import path
from .views import Home, AddAvertisement

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('add',AddAvertisement.as_view(),name='addAvertisement'),
]