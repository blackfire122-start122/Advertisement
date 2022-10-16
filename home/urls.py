from django.urls import path, include
from .views import Home, AddAvertisement, AvertisementFilter, Profile, Signup, AdvertisementUser

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('add', AddAvertisement.as_view(), name='addAvertisement'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", Profile.as_view(), name='profile'),
    path("accounts/signup", Signup.as_view(), name='signup'),
    path('ajax/add', AvertisementFilter.as_view(), name='avertisementFilter'),
    path('ajax/advertisementUser', AdvertisementUser.as_view(), name='advertisementUser'),

]
