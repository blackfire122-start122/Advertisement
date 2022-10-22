from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from .models import Category, Advertisement, Sity, ImagesAdvertisement, Company
from .forms import AdvertisementFrom, SignUpForm, ChangeForm, CompanyForm
from django.conf import settings
from django.db.models import Q
from django.shortcuts import reverse


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Categories"] = Category.objects.filter(parent__isnull=True)
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


class AvertisementFilter(TemplateView):
    template_name = 'home/ajax/avertisementFilter.html'
    advertisements = None

    def get(self, request, *args, **kwargs):
        find_on_text = request.GET.get('find_on_text')
        cities = request.GET.getlist('cities')
        category = request.GET.getlist('categories')

        filterQ = (Q(header__contains=find_on_text),)

        if cities:
            filterQ += (Q(sity__in=cities),)
        if category:
            filterQ += (Q(category__in=category),)

        self.advertisements = Advertisement.objects.filter(*filterQ)[:20]

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Advertisements"] = self.advertisements
        return context


class Profile(TemplateView):
    template_name = 'registration/profile.html'
    form = None
    errors = ''

    def get(self, request, *args, **kwargs):
        self.form = ChangeForm(instance=request.user)
        if not request.user.is_authenticated:
            return HttpResponseNotAllowed(["GET"])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            self.errors = form.errors
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["errors"] = self.errors
        return context


class Signup(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('home')


class AdvertisementUser(TemplateView):
    template_name = 'home/ajax/advertisementUser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Advertisements"] = Advertisement.objects.filter(autor=self.request.user)
        return context


class AdvertisementViews(TemplateView):
    template_name = 'home/advertisementViews.html'
    advertisement = None

    def get(self, request, *args, **kwargs):
        try:
            self.advertisement = Advertisement.objects.get(header=kwargs['name'], pk=kwargs['id'])
        except Advertisement.DoesNotExist:
            return HttpResponseNotFound()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["advertisement"] = self.advertisement
        return context


class CompanyAdd(TemplateView):
    template_name = 'home/companyAdd.html'

    form = CompanyForm
    errors = ''

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseNotAllowed(["GET"])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.company = form.save()
            request.user.save()
        else:
            self.errors = form.errors
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["errors"] = self.errors
        return context


class CompanyViews(TemplateView):
    template_name = 'home/company.html'
    company = None

    def get(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(name=kwargs['name'], pk=kwargs['id'])
        except Company.DoesNotExist:
            return HttpResponseNotFound()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context