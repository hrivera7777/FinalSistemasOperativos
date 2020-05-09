from django.shortcuts import render
from django.views.generic.base import TemplateView
#from .forms import ArchivoForm
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import  EjecArchCh #ArchivosCh,
from django.shortcuts import get_object_or_404
from .comprobar import sintax
from .ejecucion import ejecucion





#################################################################################################################3
"""

esto es update view cuidado

"""
class HomePageView(UpdateView):
    #form_class = ArchivoForm
    #model = ArchivosCh se cambió el modelo para poder recuperar la memoria y el kernel
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html"
    
    """

    esto es update view cuidado

    """

    def get(self, request, *args, **kwargs):
        #ruta=request.FILES.get('archivo')
        #nombre = ruta.name
        tup = EjecArchCh.objects.all()
        nombre=""
        memorias=[]
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
    """

    esto es update view cuidado

    """

# ########################################################################################################################




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
            nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
            memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
            kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
            tempo2= str(nombres).split('/')
            nombre=tempo2[1]
            memoriaFinal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
            kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
        
        tamMemoriaDisp = memoriaFinal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
        cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
        
        for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
            cantidMemoriaDisp.append(i+kernelFinal+1) 
        
        for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
            cantidadKernel.append(i+1) 

        instancia= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
        #print(sintax.abrirArchivo(self))    
        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'sintax':instancia.pruebaTotal(),'memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,
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
    

