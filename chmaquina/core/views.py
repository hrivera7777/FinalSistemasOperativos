from django.shortcuts import render
from django.views.generic.base import TemplateView
#from .forms import ArchivoForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import ArchivosCh
from django.shortcuts import get_object_or_404





class HomePageView(UpdateView):
    #form_class = ArchivoForm
    model = ArchivosCh
    fields = ['archivo']
    success_url= reverse_lazy('home')
    template_name = "core/base.html"
    
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'title': "Ch Máquina"})
    """
    def get_object(self, queryset=None):
        return get_object_or_404(ArchivosCh)
    """
    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        profile, created= ArchivosCh.objects.get_or_create()
        return profile
    
# Create your views here.
