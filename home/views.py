from django.views.generic.base import TemplateView
from .models import Category, Advertisement, Sity, ImagesAdvertisement
from .forms import AdvertisementFrom
from django.conf import settings


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Categories"] = Category.objects.filter(parent__isnull=True)
        context["Advertisement"] = Advertisement.objects.all()[:20]
        context["Cities"] = Sity.objects.all()
        return context


class AddAvertisement(TemplateView):
    template_name = 'home/addAvertisement.html'

    form = AdvertisementFrom()
    errors = ''

    def post(self, request, *args, **kwargs):
        if len(request.FILES.getlist('images')) > settings.MAX_FILES_LOAD:
            self.errors = "Max files " + str(settings.MAX_FILES_LOAD)
            return super().get(request, *args, **kwargs)

        correct_files = True
        for i in request.FILES.getlist('images'):
            correct_files = False
            for e in settings.FILE_FORMATS:
                if i.name.endswith(e):
                    correct_files = True
            if not correct_files:
                self.errors = 'File format not correct'
                return super().get(request, *args, **kwargs)

        self.form = AdvertisementFrom(request.POST)

        if self.form.is_valid():
            advertisement = self.form.save()
            for i in request.FILES.getlist('images'):
                img = ImagesAdvertisement(img=i)
                img.save()
                advertisement.images.add(img)
        else:
            self.errors = self.form.errors
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["errors"] = self.errors
        return context
