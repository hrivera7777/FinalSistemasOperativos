from django.shortcuts import render
from django.views.generic.base import TemplateView
#from .forms import ArchivoForm
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import  EjecArchCh #ArchivosCh,
from django.shortcuts import get_object_or_404
from .comprobar import sintax
from .ejecucion import ejecucion





class HomePageView(UpdateView):
    #form_class = ArchivoForm
    #model = ArchivosCh se cambió el modelo para poder recuperar la memoria y el kernel
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html"
    
    
    def get(self, request, *args, **kwargs):
        #ruta=request.FILES.get('archivo')
        #nombre = ruta.name
        tup = EjecArchCh.objects.all()
        nombre=""
        for tp in tup:
            nombres=tp.archivo
            tempo2= str(nombres).split('/')
            nombre=tempo2[1]
        instancia= sintax()
        #print(sintax.abrirArchivo(self))    
        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'sintax':instancia.pruebaTotal()}) # })#,
        #'sintax':instancia.abrirArchivo()
    """
    def get_object(self, queryset=None):
        return get_object_or_404(ArchivosCh)
    """
    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        #profile, created= ArchivosCh.objects.get_or_create()
        profile, created= EjecArchCh.objects.get_or_create()
        return profile
    
# Create your views here.
## con esta view permite agregar varios archivos ch a la vez 
class HomePageView2(CreateView):
    #form_class = ArchivoForm
    #model = ArchivosCh se cambió el modelo para poder recuperar la memoria y el kernel
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html"
    
    
    def get(self, request, *args, **kwargs):
        #ruta=request.FILES.get('archivo')
        #nombre = ruta.name
        tup = EjecArchCh.objects.all()
        nombre=""
        for tp in tup:
            nombres=tp.archivo
            tempo2= str(nombres).split('/')
            nombre=tempo2[1]
        instancia= sintax()
        #print(sintax.abrirArchivo(self))    
        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'sintax':instancia.pruebaTotal()}) # })#,
        #'sintax':instancia.abrirArchivo()
    """
    def get_object(self, queryset=None):
        return get_object_or_404(ArchivosCh)
    """
    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        #profile, created= ArchivosCh.objects.get_or_create()
        profile, created= EjecArchCh.objects.get_or_create()
        return profile
    
# Create your views here.

