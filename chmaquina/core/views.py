from django.shortcuts import render
from django.views.generic.base import TemplateView
#from .forms import ArchivoForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import ArchivosCh
from django.shortcuts import get_object_or_404
from .comprobar import sintax





class HomePageView(UpdateView):
    #form_class = ArchivoForm
    model = ArchivosCh
    fields = ['archivo']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html"
    
    
    def get(self, request, *args, **kwargs):
        #ruta=request.FILES.get('archivo')
        #nombre = ruta.name
        tup = ArchivosCh.objects.all()
        for tp in tup:
            nombres=tp.archivo
            tempo2= str(nombres).split('/')
            nombre=tempo2[1]
        instancia= sintax()
        #print(sintax.abrirArchivo(self))    
        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'sintax':instancia.pruebaTotal()})
        #'sintax':instancia.abrirArchivo()
    """
    def get_object(self, queryset=None):
        return get_object_or_404(ArchivosCh)
    """
    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        profile, created= ArchivosCh.objects.get_or_create()
        return profile
    
# Create your views here.
