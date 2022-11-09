from django.urls import path, include
from .views import Home, AddAvertisement, Profile, Signup, AdvertisementUser, AdvertisementViews,\
    CompanyAdd, CompanyViews, login_redirect, CompanyChange, CompaniesFilter
from .ajax_views import AvertisementFilter


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('addAvertisement', AddAvertisement.as_view(), name='addAvertisement'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<str:name>/<int:id>', Profile.as_view(), name='profile'),
    path('login_redirect', login_redirect, name='login_redirect'),
    path('accounts/signup', Signup.as_view(), name='signup'),
    path('advertisement/<str:name>/<int:id>', AdvertisementViews.as_view(), name='advertisement'),
    path('company/<str:name>/<int:id>', CompanyViews.as_view(), name='company'),
    path('companyadd', CompanyAdd.as_view(), name='company_add'),
    path('Change/company/<str:name>/<int:id>', CompanyChange.as_view(), name='company_change'),
    path('api/v1/advertisementFilter', AvertisementFilter.as_view(), name='avertisementFilter'),
    path('ajax/advertisementUser', AdvertisementUser.as_view(), name='advertisementUser'),
    path('ajax/CompaniesFilter', CompaniesFilter.as_view(), name='companiesFilter'),

]
