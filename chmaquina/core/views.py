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

        instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
        #print(sintax.abrirArchivo(self))
        instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay

        if instanciaSintaxis.hayError():  
            ## se mostraría el error que tiene el programa .ch
            return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,
            
        else:
            # se continua con la ejecucion
            instanciaEjec = ejecucion()
            if not(instanciaEjec.puedeEjecKernel()):
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'no hay suficiente espacio para el kernel con respecto al tamaño de la memoria','memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,
            else:
                instanciaEjec.agregarKernelMemoria()
                if not(instanciaEjec.puedeEjecProg()):
                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'no hay suficiente espacio para el programa con respecto al tamaño de la memoria','memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,
                else:
                    instanciaEjec.agregarInstrMemoria()
                    instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                    #se con el llamado de todos los metodos para mostrar todos los datos en el frontend
                    pant = instanciaEjec.getPantalla() # (str) datos pantalla en el frontend
                    impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                    acum = instanciaEjec.getAcumulador() # (str) 
                    linAct = instanciaEjec.getLineaActual() # (str) 
                    codProAct = instanciaEjec.getCodProgActualMod() # (list) 
                    #posCodProAct = instanciaEjec.getCodProgActualMod() # (list) #getCodProgActualMod
                    varAct = instanciaEjec.getVariablesActuales()# (list) 
                    posVarAct = instanciaEjec.getPosVariablesActuales() # (list) 
                    etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                    posEtiqAct = instanciaEjec.getPosEtiquetasActuales() # (list) 
                    mem = instanciaEjec.getMemoria() # (list) 
                    #posMem = instanciaEjec.getPosMemoria() # (list) 
                    prog = instanciaEjec.getProgramas() # (list) 
                    idPr = instanciaEjec.getIdProg() # (list)
                    cantInsProg = instanciaEjec.getCanInstProg() # int
                    regBas= instanciaEjec.getRegistroBase() # (list) 
                    regLimCod = instanciaEjec.getRegistroLimCod() # (list) 
                    regLimPro = instanciaEjec.getRegistroLimProg() # (list) 
                    memDis = instanciaEjec.getMemoriaDispo() # (list) 
                    
                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaFinal': memDis, 'kernel': cantidadKernel, 
                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varActi':{'varAct': varAct,
                                    'posVarAct':posVarAct}, 'etiqActi':{'etiqAct': etiqAct, 'posEtiqAct': posEtiqAct}, 'memo':{'mem':mem,},
                                    'proga':{'prog':prog , 'idPr':idPr,'cantInsProg':cantInsProg, 'regBas':regBas, 'regLimCod':regLimCod, 'regLimPro':regLimPro},
                    
                                    }) # })#,  'posMem':posMem,}, #'codProActi': {'codProAct': codProAct,"posCodProAct": posCodProAct} "posCodProAct": posCodProAct,

            #return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'puede continuar a la ejecución','memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,

        
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
    

