from django.views.generic.base import TemplateView
from .models import Category, Advertisement, Sity

class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Categories"] = Category.objects.filter(parent__isnull=True)
        context["Advertisement"] = Advertisement.objects.all()[:20]
        context["Cities"] = Sity.objects.all()
        return context