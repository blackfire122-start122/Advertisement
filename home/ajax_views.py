from rest_framework.generics import ListAPIView
from .models import Advertisement
from .serializers import AdvertisementFilterSerializer
from django.db.models import Q
from rest_framework.exceptions import NotFound
from django.conf import settings


class AvertisementFilter(ListAPIView):
    serializer_class = AdvertisementFilterSerializer

    def get_queryset(self):
        if not self.request.GET.get('start') or not self.request.GET.get('end'):
            raise NotFound()
        if not self.request.GET.get('start').isdigit() or not self.request.GET.get('end').isdigit():
            raise NotFound()
        if int(self.request.GET.get('end')) - int(self.request.GET.get('start')) > settings.MAX_AJAX_GET:
            raise NotFound()

        find_on_text = self.request.GET.get('find_on_text')
        cities = self.request.GET.getlist('cities')
        category = self.request.GET.getlist('categories')
        companies = self.request.GET.getlist('companies')
        filterQ = (Q(is_active=True),)

        if find_on_text:
            filterQ += (Q(header__contains=find_on_text),)
        if cities:
            filterQ += (Q(sity__in=cities),)
        if category:
            filterQ += (Q(category__in=category),)
        if companies:
            filterQ += (Q(company__in=companies),)

        return Advertisement.objects.filter(*filterQ)[int(self.request.GET.get('start')):int(self.request.GET.get('end'))]
