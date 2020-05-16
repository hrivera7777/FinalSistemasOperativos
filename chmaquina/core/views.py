from django.shortcuts import render
from django.views.generic.base import TemplateView
#from .forms import ArchivoForm
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import  EjecArchCh #ArchivosCh,
from django.shortcuts import get_object_or_404
from .comprobar import sintax
from .ejecucion import ejecucion
from django.core.files import File # se hace necesario para la apertura del archivo

import json
from django.http import HttpResponse
from django.http import JsonResponse # ultimo agregado





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
        """
        tup = EjecArchCh.objects.all()
        nombre=""
        for tp in tup:
            nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
            memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
            kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
            tempo2= str(nombres).split('/')
            nombre=tempo2[1]
            memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
            kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
        
        tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
        cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
        
        for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
            cantidMemoriaDisp.append(i+kernelFinal+1) 
        
        for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
            cantidadKernel.append(i+1) 
        """

        
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
        #print(ejecute,'este es el valor de ejecute - ' , type(ejecute))

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['presione abir y cargue un archivo .ch, así también cargará el tamaño de la memoria y el tamaño del kernel'],'modo':'Modo kernel'}) # })#,   
           
        else:
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch

            if str(ejecute) == 'ejecutarOk':
                nombre=""
                tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
                ruta=[]
                for tp in tup: 
                    nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                    ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                    memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                    kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                    tempo2= str(nombres).split('/')
                    nombre=tempo2[1]
                    memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                    kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
                
                    tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                    cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                    cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  

                ##################################################################
                proEjec=len(ruta)-1 # este será el programa que se ejecutará, el ultimo programa que fue agregado a la base de datos
                #print(proEjec, 'esto es progEje ')
                #print(ruta,'esto es ruta')
                
                f="" #se utiliza para abrir el archivo desde la ruta relativa
                myfile ="" #se utiliza para crear una instancia de la clase file y así tener un manejo desde django
                leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
                
                #aqui tratamos de leer el archivo si es posible.
                try:
                    f = open("media/" + ruta[proEjec], "r")
                    myfile = File(f)
                    #print(myfile)
                    leer = myfile.readlines() #para leer linea a linea #print(leer)
                    f.close()
                    myfile.close()
                    #print(leer)
                except:
                    print('no se puede abrir el archivo solicitado')  

                #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
                leerLimp=[] 
                for w in range(len(leer)):
                    leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
                
                #leerLimp = filter(None, leerLimp)
                #leerLimp :[item for item in leerLimp if len(item)>0]
                leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista
                #print(leerLimp, 'limp')
                ####################################################################

                instanciaArch = cargArchivo(tup, nombres, memoriaTotal, kernelFinal, ruta, leer, proEjec)

                instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
                
                instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 

                instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
                
                instanciaEjec.setCantMemo(int(instanciaArch.getMemoriaDB())) # se envia la cantidad de memoria a la ejecución
                instanciaEjec.setKernel(int(instanciaArch.getKernelBD())) # se envia la cantidad de kernel a la ejecución
                instanciaEjec.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
                #instanciaEjec.setProgEjec(int(instanciaArch.getProgEjecBD())) # se envia el programa a ser ejecutado a la ejecución
                instanciaEjec.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
                instanciaEjec.setRuta(instanciaArch.getRutaBD()) # se envia las rutas de los archivos a la ejecución
                pant = instanciaEjec.getPantalla()

                if not(instanciaEjec.puedeEjecKernel()):
                    for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                        cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['no hay suficiente espacio para el kernel con respecto al tamaño de la memoria'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
                
                else:
                    instanciaEjec.agregarKernelMemoria()
                    for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                        cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                    for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                        cantidadKernel.append(i+1) 
                    """
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)
                    """
                    if not(instanciaEjec.puedeEjecProg()) and request.method == 'GET':
                            return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['no hay suficiente espacio para el programa con respecto al tamaño de la memoria'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                    else:
                        instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                        if instanciaSintaxis.hayError():  
                            ## se mostraría el error que tiene el programa .ch
                            return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                        else:
                            instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                            instanciaEjec.setContinuarLeyendo(True)
                            #instanciaEjec.playHppal()
                            instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                            instanciaEjec.setValoraLeer(30)
                            instanciaEjec.setContinuarLeyendo(False)

                            #print('entre aqui')
                            #instanciaEjec.agregarEtiquetas() # agrega las etiquetas para poder ser referenciadas
                            
                            #if request.method == 'GET':
                            #    instanciaEjec.setValoraLeer(request.GET.get('ModalInput')) 
                            #else:
                            #    instanciaEjec.setValoraLeer(str(10)) 
                            """
                            cont=0
                            
                            for i in range(len(leerLimp2)):
                                #palabras = self.leer[i].rstrip().split()
                                palabras = leerLimp2[i].rstrip().split()
                                #print(palabras, 'esto es palabras')
                                #print(palabras)
                                operador = palabras[0]
                                if operador == 'lea':
                                    cont +=1
                                    break
                                else:
                                    continue
                                    
                            for i in range(cont):
                                print('entró al if que está en el else, el valor de actiModal')
                                actiModal = False
                                #print('entró al if que está en el else, el valor de actiModal 2', str(actiModal))
                                instanciaEjec.setActivarVentLeer(False)
                                cont=0
                                return JsonResponse({'actiModal':True})


                            """


                            #actiModal = instanciaEjec.getActivarVentLeer() # bolean
                            #if contado == 1:
                            #    actiModal = instanciaEjec.getActivarVentLeer() # bolean 
                            #    contado +=1
                            #else:
                            #    actiModal = not(instanciaEjec.getActivarVentLeer())
                            #actiModal = False
                            """
                            if actiModal:
                                print('entró al if que está en el else, el valor de actiModal', str(actiModal))
                                actiModal = False
                                #print('entró al if que está en el else, el valor de actiModal 2', str(actiModal))
                                instanciaEjec.setActivarVentLeer(False)
                                return JsonResponse({'actiModal':True})
                            """

                            #elif request.GET.get('ModalInput') != '':
                            """
                            if request.method == 'GET':
                                print('elif')
                                instanciaEjec.setValoraLeer(10) # linea nueva 
                                print(request.GET.get('ModalInput'), 'esto  lo que está en la modal')
                                instanciaEjec.continuarLeyendo(not(request.method == 'GET')) #debe enviar un false, ya se abrio la ventana modal
                                #actiModal = instanciaEjec.getActivarVentLeer()
                                
                                
                                
                                
                                
                                #se con el llamado de todos los metodos para mostrar todos los datos en el frontend
                                pant = instanciaEjec.getPantalla() # (str) datos pantalla en el frontend
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 


                                #posCodProAct = instanciaEjec.getCodProgActualMod() # (list) #getCodProgActualMod
                                #posVarAct = instanciaEjec.getPosVariablesActuales() # (list) 
                                #posEtiqAct = instanciaEjec.getPosEtiquetasActuales() # (list) 
                                #posMem = instanciaEjec.getPosMemoria() # (list) 
                                #idPr = instanciaEjec.getIdProg() # (list)
                                #cantInsProg = instanciaEjec.getCanInstProg() # int
                                #regBas= instanciaEjec.getRegistroBase() # (list) 
                                #regLimCod = instanciaEjec.getRegistroLimCod() # (list) 
                                #regLimPro = instanciaEjec.getRegistroLimProg() # (list) 
                                
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,}) 
                                                # })#,  'posMem':posMem,}, #'codProActi': {'codProAct': codProAct,"posCodProAct": posCodProAct}, 'varActi':{'posVarAct':posVarAct}, 'etiqActi':{'posEtiqAct': posEtiqAct},
                                                                            #'proga':{'prog':prog , 'idPr':idPr,'cantInsProg':cantInsProg, 'regBas':regBas, 'regLimCod':regLimCod, 'regLimPro':regLimPro}, 'memo':{
                            
                            else:
                            """
                            #actiModal = False
                            #instanciaEjec.setValoraLeer(request.GET.get('ModalInput')) # linea nueva 
                            #print(request.GET.get('ModalInput'), 'esto  lo que está en la modal')
                            #print('ultimo else')
                            #se con el llamado de todos los metodos para mostrar todos los datos en el frontend
                            pant = instanciaEjec.getPantalla() # (str) datos pantalla en el frontend
                            impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                            acum = instanciaEjec.getAcumulador() # (str) 
                            linAct = instanciaEjec.getLineaActual() # (str) 
                            codProAct = instanciaEjec.getCodProgActual() # (list) 
                            varAct = instanciaEjec.getVariablesActuales()# (list) 
                            etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                            mem = instanciaEjec.getMemoria() # (list) 
                            prog = instanciaEjec.getProgramas() # (list) 
                            memDis = instanciaEjec.getMemoriaDispo() # (list) 


                            #posCodProAct = instanciaEjec.getCodProgActualMod() # (list) #getCodProgActualMod
                            #posVarAct = instanciaEjec.getPosVariablesActuales() # (list) 
                            #posEtiqAct = instanciaEjec.getPosEtiquetasActuales() # (list) 
                            #posMem = instanciaEjec.getPosMemoria() # (list) 
                            #idPr = instanciaEjec.getIdProg() # (list)
                            #cantInsProg = instanciaEjec.getCanInstProg() # int
                            #regBas= instanciaEjec.getRegistroBase() # (list) 
                            #regLimCod = instanciaEjec.getRegistroLimCod() # (list) 
                            #regLimPro = instanciaEjec.getRegistroLimProg() # (list) 
                            
                            
                            return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,}) 
                                            # })#,  'posMem':posMem,}, #'codProActi': {'codProAct': codProAct,"posCodProAct": posCodProAct}, 'varActi':{'posVarAct':posVarAct}, 'etiqActi':{'posEtiqAct': posEtiqAct},
                                                                        #'proga':{'prog':prog , 'idPr':idPr,'cantInsProg':cantInsProg, 'regBas':regBas, 'regLimCod':regLimCod, 'regLimPro':regLimPro}, 'memo':{                                                           
            
            else:
                return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['presione ejecutar para comenzar'],'modo':'Modo kernel'}) # })#,   









        """
        if instanciaSintaxis.hayError():  
            ## se mostraría el error que tiene el programa .ch
            return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)
       

        else:
            # se continua con la ejecucion
            instanciaEjec = ejecucion()
            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL

                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'no hay suficiente espacio para el kernel con respecto al tamaño de la memoria','memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,
            else:
                instanciaEjec.agregarKernelMemoria()
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                if not(instanciaEjec.puedeEjecProg()):
                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'no hay suficiente espacio para el programa con respecto al tamaño de la memoria','memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,
                
                
                else:
                    instanciaEjec.agregarInstrMemoria()
                    instanciaEjec.agregarEtiquetas()
                    instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                    #se con el llamado de todos los metodos para mostrar todos los datos en el frontend
                    pant = instanciaEjec.getPantalla() # (str) datos pantalla en el frontend
                    impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                    acum = instanciaEjec.getAcumulador() # (str) 
                    linAct = instanciaEjec.getLineaActual() # (str) 
                    codProAct = instanciaEjec.getCodProgActual() # (list) 
                    #posCodProAct = instanciaEjec.getCodProgActualMod() # (list) #getCodProgActualMod
                    varAct = instanciaEjec.getVariablesActuales()# (list) 
                    #posVarAct = instanciaEjec.getPosVariablesActuales() # (list) 
                    etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                    #posEtiqAct = instanciaEjec.getPosEtiquetasActuales() # (list) 
                    mem = instanciaEjec.getMemoria() # (list) 
                    #posMem = instanciaEjec.getPosMemoria() # (list) 
                    prog = instanciaEjec.getProgramas() # (list) 
                    #idPr = instanciaEjec.getIdProg() # (list)
                    #cantInsProg = instanciaEjec.getCanInstProg() # int
                    #regBas= instanciaEjec.getRegistroBase() # (list) 
                    #regLimCod = instanciaEjec.getRegistroLimCod() # (list) 
                    #regLimPro = instanciaEjec.getRegistroLimProg() # (list) 
                    memDis = instanciaEjec.getMemoriaDispo() # (list) 
                    
                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                    'etiqAct': etiqAct, 'memo':{'mem':mem,}, 'modo':'Modo usuario', 'prog':prog,
                                    }) # })#,  'posMem':posMem,}, #'codProActi': {'codProAct': codProAct,"posCodProAct": posCodProAct}, 'varActi':{'posVarAct':posVarAct}, 'etiqActi':{'posEtiqAct': posEtiqAct},
                                                                  #'proga':{'prog':prog , 'idPr':idPr,'cantInsProg':cantInsProg, 'regBas':regBas, 'regLimCod':regLimCod, 'regLimPro':regLimPro},

            #return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':'puede continuar a la ejecución','memoriaFinal': cantidMemoriaDisp, 'kernel': cantidadKernel}) # })#,

         """
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
    

class cargArchivo(): #clase que hace de puente para enviar los datos para la sintaxis o la ejecución 

    #tup2 = EjecArchCh.objects.all()
    tup =[]
    ruta=[""] #aqui se agregan todos los archivos para abrir 
    cantmemoria= 0
    kernel= 0
    
    #proEjec=len(tup)-1
    proEjec = 0

    tempo=""
    nombre2=""
    tp =[]
    
    """
    for tp in tup:
        print()
        ruta.append(str(nombre2))
    """

    """
    for tp in tup:
        nombre2=tp.archivo
        tempo = tp.memoria
        cantmemoria=int(tempo) # cantidad total de memoria, se va disminuyendo si se agrega el kernel o programas
        tempo = tp.kernel
        kernel=int(tempo)
        ruta.append(str(nombre2))
        tempo = tp.id 
        #print(tempo)
        #proEjec= int(tempo)
    """

    """
    f=""
    myfile =""
    leer=[]
    try:
        f = open("media/" + ruta[proEjec], "r")
        myfile = File(f)
        print(myfile)
        leer = myfile.readlines() #para leer linea a linea #print(leer)
        f.close()
        myfile.close()
    except:
        print('no se puede abrir el archivo solicitado')
    """

    def __init__(self,arregloBd, nombre, cantMemoria, kernel, ruta, leer, proEjec):
        self.tup = arregloBd # con esto recuperamos todos los datos desde la bd
        self.cantmemoria = cantMemoria
        self.nombre2 = nombre
        self.kernel = kernel
        self.ruta = ruta
        self.leer = leer 



    def getArchivoBD(self): # retorna todas las lineas del archivo .ch
        return self.leer
    
    def getMemoriaDB(self): # retorna la cantidad de memoria del programa en ejecucion 
        return self.cantmemoria
    
    def getKernelBD(self): # retorna cantidad de memoria del programa en ejecucion 
        return self.kernel

    def getProgEjecBD(self): # retorna el programa en ejecucion 
        return self.proEjec

    def getRutaBD(self): # retorna la lista de programas en la bd 
        return self.ruta

    
    