from django.urls import path
from .views import Home, AddAvertisement, AvertisementFilter


urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('add', AddAvertisement.as_view(), name='addAvertisement'),
    path('ajax/add', AvertisementFilter.as_view(), name='avertisementFilter'),
]