from django.views.generic.base import TemplateView
from django.http import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseForbidden
from .models import Category, Advertisement, Sity, ImagesAdvertisement, Company, User
from .forms import AdvertisementFrom, SignUpForm, ChangeForm, CompanyForm, ChangeCompanyForm
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Categories"] = Category.objects.filter(parent__isnull=True)
        context["Cities"] = Sity.objects.all()
        context["Companies"] = Company.objects.all()[:20]
        return context


class AddAvertisement(TemplateView):
    template_name = 'home/addAvertisement.html'

    form = AdvertisementFrom()
    errors = ''

    def post(self, request, *args, **kwargs):
        # company emails check
        if len(User.objects.filter(email=request.POST['email'])) > 0 or\
                len(Company.objects.filter(email=request.POST['email'])):
            self.errors = 'Such email already use'
            return super().get(request, *args, **kwargs)

        if len(request.FILES.getlist('images')) > settings.MAX_FILES_LOAD:
            self.errors = "Max files " + str(settings.MAX_FILES_LOAD)+"\n"
            return super().get(request, *args, **kwargs)

        # check files
        for i in request.FILES.getlist('images'):
            correct_files = False
            for e in settings.FILE_FORMATS:
                if i.name.endswith(e):
                    correct_files = True
            if not correct_files:
                self.errors = 'File format not correct'
                return super().get(request, *args, **kwargs)

        self.form = AdvertisementFrom(request.POST)
        # save
        if self.form.is_valid():
            advertisement = self.form.save()
            for i in request.FILES.getlist('images'):
                img = ImagesAdvertisement(img=i)
                img.save()
                advertisement.images.add(img)
            advertisement.autor = request.user
            advertisement.save()
            # send_email need realise
        else:
            self.errors += self.form.errors
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["errors"] = self.errors
        return context


class Profile(TemplateView):
    template_name = 'registration/profile.html'
    form = None
    errors = ''
    other = None

    def get(self, request, *args, **kwargs):
        try:
            self.other = User.objects.get(username=kwargs['name'], pk=kwargs['id'])
        except User.DoesNotExist:
            return HttpResponseNotFound()

        if self.other == request.user:
            self.form = ChangeForm(instance=request.user)

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
        context['other'] = self.other
        return context


class Signup(TemplateView):
    form = SignUpForm()
    template_name = 'registration/signup.html'
    errors = ''

    def post(self, request, *args, **kwargs):
        # check email
        if len(User.objects.filter(email=request.POST['email'])) > 0 or\
                len(Company.objects.filter(email=request.POST['email'])):
            self.errors = 'Such email already use'
            return super().get(request, *args, **kwargs)
        self.form = SignUpForm(request.POST)

        if self.form.is_valid():
            self.form.save()
            # send_email
            return redirect('home')
        else:
            self.errors = self.form.errors
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["errors"] = self.errors
        return context


class AdvertisementUser(TemplateView):
    template_name = 'home/ajax/advertisementUser.html'
    advertisements = None

    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET.get('user') == request.user.username:
                self.advertisements = Advertisement.objects.filter(autor=self.request.user)
            else:
                self.advertisements = Advertisement.objects.filter(
                    autor=User.objects.get(
                        username=self.request.GET.get('user'),
                        pk=self.request.GET.get('id')
                    )
                )
        except (Advertisement.DoesNotExist, User.DoesNotExist):
            return HttpResponseNotFound()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Advertisements"] = self.advertisements
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
            request.user.companies.add(form.save())
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


class CompanyChange(TemplateView):
    template_name = 'home/companyChange.html'
    company = None
    form = ChangeCompanyForm
    errors = ''

    def check(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(name=kwargs['name'], pk=kwargs['id'])
        except Company.DoesNotExist:
            return False, HttpResponseNotFound()
        if self.company not in request.user.companies.all():
            return False, HttpResponseForbidden()
        return True,

    def get(self, request, *args, **kwargs):
        res = self.check(request, *args, **kwargs)
        if not res[0]:
            return res[1]

        self.form = ChangeCompanyForm(instance=self.company)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res = self.check(request, *args, **kwargs)
        if not res[0]:
            return res[1]

        form = ChangeCompanyForm(request.POST, request.FILES, instance=self.company)
        if form.is_valid():
            form.save()
        else:
            self.errors = form.errors
        return redirect('company', name=self.company, id=self.company.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = self.form
        context["errors"] = self.errors
        return context


@login_required
def login_redirect(request):
    return redirect('profile', name=request.user.username, id=request.user.pk)
