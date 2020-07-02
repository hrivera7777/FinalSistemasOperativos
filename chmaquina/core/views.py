from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import  EjecArchCh #ArchivosCh,
#from django.shortcuts import get_object_or_404
from .comprobar import sintax
from .ejecucion import ejecucion
from .pasoapaso import PaP
from django.core.files import File # se hace necesario para la apertura del archivo
from .memoria import memoria
import os
import random
from collections import deque

#import json
#from django.http import HttpResponse
#from django.http import JsonResponse # ultimo agregado


# ########################################################################################################################
##########################################################################################################################


contadorPasos =0 # se utiliza para la realizar la ejecucion paso a paso
cambioCurso = False
ActivarVentLeer = False
ActivarVentLeerPaP = False
varALeer = []
varALeerPaP =[]
cuantosLea = 0
cuantosLeaFaltan = -1
listaValoresVariTeclado = []
listaValoresVariTecladoPaP = []
tieneQueLeerPaP= -2
#todasInstancias =[]
colaP = deque() # para agregar los procesos que van llegando en FCFS
dicProc={} # para agregar los procesos que llegan para los nuevos algoritmos de planificación de procesos
proEjec=0
entro=0
dicTRafagaLinea={}
## con esta view permite agregar varios archivos ch a la vez 
#algoritomo FCFS
class HomePageView2(CreateView):
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('fcfs')
    template_name = "core/base.html"
    global cambioCurso
    global ActivarVentLeer
    global ActivarVentLeerPaP
    global varALeer
    global varALeerPaP
    global cuantosLea
    global cuantosLeaFaltan
    global tieneQueLeerPaP
    global proEjec

    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self, leer,proEjec, cantmemoriaConKernel, cantMemoriaTotal, tamMemoriaConProg):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(leer)):
            palabras = leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if proEjec == 0:
            if cantmemoriaConKernel >= (len(leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (cantMemoriaTotal - tamMemoriaConProg) >= (len(leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def abrirArch(self, ruta):
        f="" #se utiliza para abrir el archivo desde la ruta relativa
        leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
        
        #aqui tratamos de leer el archivo si es posible.
        try:
            f = open("media/" + ruta, "r")
            #myfile = File(f)
            leer = f.readlines() #para leer linea a linea
            f.close()
            #myfile.close()
        except:
            print('no se puede abrir el archivo solicitado')  

        #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
        leerLimp=[] 
        for w in range(len(leer)):
            leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
        
        leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista

        return leerLimp2


    def get(self, request, *args, **kwargs):
        global contadorPasos
        global cambioCurso
        global proEjec
        global entro
        leerLimp2=[] 
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
 

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione abir y cargue un archivo .ch, así, también cargará el tamaño de la memoria y el tamaño del kernel.'],'modo':'Modo kernel'}) # })#,   
           
        else:
            entro +=1
            print("esto es proEjec", proEjec)
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch
            pasoaPaso = request.GET.get('pasoapaso')
            sgtPaso = request.GET.get('sgtpaso')
            variablePorTeclado = request.GET.get('leaTeclado')
            variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
         
            nombre=""
            tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
            ruta=[]
            nombreArchivos=[]
            for tp in tup:

                nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                tempo2= str(nombres).split('/')
                nombreArchivos.append(tempo2[1])
                memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
            
                tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
            
            nombre=nombreArchivos[proEjec] #nombre del archivo que se muestra en el front
            
            
            ##################################################################
            #20-06-2020 proEjec=len(ruta)-1 # este será el programa que se ejecutará, el ultimo programa que fue agregado a la base de datos
            global colaP
            print('entro', entro,"\n")
            if entro == len(ruta) or contadorPasos>0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
                colaP.clear
            
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")

                leerLimp2= self.abrirArch(rutaPrograma)
                #colaP.pop()
                colaP.appendleft(leerLimp2)
                Calcular.Rafaga(leerLimp2)
            print("cola inicio",colaP)

            """ 20-06-2020
            f="" #se utiliza para abrir el archivo desde la ruta relativa
            #myfile ="" #se utiliza para crear una instancia de la clase file y así tener un manejo desde django
            leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
            
            #aqui tratamos de leer el archivo si es posible.
            try:
                f = open("media/" + ruta[proEjec], "r")
                #myfile = File(f)
                leer = f.readlines() #para leer linea a linea
                f.close()
                #myfile.close()
            except:
                print('no se puede abrir el archivo solicitado')  

            #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
            leerLimp=[] 
            for w in range(len(leer)):
                leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
            
            leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista
            """
            
            #tempoLeer= colaP.pop() # se usa para tomar el ultimo proceso que llegó 
           
            ####################################################################
            #global todasInstancias #podría removerse
            
            instanciaMemoria = memoria(int(memoriaTotal),int(kernelFinal))

            #############################################################################################################
            instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
            #todasInstancias.append(instanciaSintaxis)

            instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
            ###############################################################################################


            instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
            instanciaPaP = PaP() # se crea una instancia de la clase paso a paso para poder llamar los metodos necesarios para la ejecucion paso a paso

            if proEjec==0 and entro==1: # se necesita para cuando se sale del programa chmaquina y se vuelve a ingresar 
                instanciaEjec.clean()
                instanciaPaP.clean()
            #todasInstancias.append(instanciaEjec)
            #######################################################################
            instanciaEjec.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaEjec.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
           # instanciaEjec.setLeer(tempoLeer) # se envia la lista con todas la lineas a ejecucion 
            instanciaEjec.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
            instanciaEjec.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ########################################################################
           
            
            #todasInstancias.append(instanciaPaP)
            ########################################################################
            instanciaPaP.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaPaP.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
            #instanciaPaP.setLeer(tempoLeer) # se envia la lista con todas la lineas a paso a paso 
            #instanciaPaP.setLeer(leerLimp2) # se envia la lista con todas la lineas a paso a paso 
            instanciaPaP.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
            instanciaPaP.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            #cambioCurso = instanciaPaP.getCambiaCurso()
            #print(cambioCurso, 'cambioCurso linea 232')
            ##########################################################################

            

            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el kernel con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
            
            else:
                #instanciaMemoria.agregarKernelMemoria() 07-06-2020
                instanciaEjec.agregarKernelMemoria()

                if contadorPasos ==0 and proEjec == 0 and not(cambioCurso):
                    instanciaPaP.agregarKernelMemoria()

                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                #if not(instanciaMemoria.puedeEjecProg()) and request.method == 'GET': 07-06-2020
                if not(self.puedeEjecProg(leerLimp2, proEjec,(memoriaTotal-kernelFinal),memoriaTotal,instanciaEjec.getTamMemoriaKernelProg())) and request.method == 'GET':
                #if not(instanciaEjec.puedeEjecProg()) and request.method == 'GET':
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el programa con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                else:
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                    else:
                        ######################################################
                        if request.GET.get('leaTeclado') == None:
                            varPrev = ""
                        else:
                            varPrev = request.GET.get('leaTeclado')
                        if request.GET.get('leaTecladoPaP') == None:
                            varPrevPaP = ""
                        else:
                            varPrevPaP = request.GET.get('leaTeclado')
                        ##############################################

                       
                        if str(ejecute) == 'ejecutarOk' or varPrev !='': 
                            
                            global varALeer
                            global varALeerPaP
                            global cuantosLea
                            global cuantosLeaFaltan
                            global listaValoresVariTeclado
                            global listaValoresVariTecladoPaP
                            lineaCod = ""
                            operando = ""

                            for i in range(len(leerLimp2)):
                                
                                try:
                                    lineaCod = leerLimp2[i].split()
                                    operando = lineaCod[0]
                                except :
                                    lineaCod = ""
                                    operando = ""
                                
                                if operando == 'lea': 
                                    varALeer.append(lineaCod[1])
                                    cuantosLea +=1 
                                
                            varALeer.reverse()
                            global ActivarVentLeer 
                         


                            if cuantosLeaFaltan == -1 and cuantosLea > 0 :
                                print('entré primer if')
                                cuantosLeaFaltan = cuantosLea
                                ActivarVentLeer = True 
                                cuantosLeaFaltan -=1

                                
                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':varALeer.pop()}) 
                                
                            elif varPrev !='' and cuantosLeaFaltan > 0:
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)
                                
                                if cuantosLeaFaltan > 0:
                                    ActivarVentLeer = True
                                    print('se volvio True')
                                else :
                                    print('se volvio false')
                                    ActivarVentLeer = False
                                cuantosLeaFaltan -=1

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                try:
                                    variable =varALeer.pop()
                                except:
                                    variable = "" 
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':variable}) 
                            
                            elif cuantosLeaFaltan == 0 :
                                ActivarVentLeer = False 
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)

                                instanciaEjec.setValoraLeer(listaValoresVariTeclado) ##despues de leer todos los valores
                                
                                tempoLeer= colaP.pop() # se usa para tomar el ultimo proceso que llegó 
                                instanciaEjec.setLeer(tempoLeer) # se envia la lista con todas la lineas a ejecucion 

                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 

                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 

                            else:
                                tempoLeer= colaP.pop() # se usa para tomar el ultimo proceso que llegó 
                                #print("esto es leer", tempoLeer, 'programa', proEjec)
                                #print("esto queda en la cola",colaP)
                                instanciaEjec.setLeer(tempoLeer) # se envia la lista con todas la lineas a ejecucion 
                                
                                ActivarVentLeer = False
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                proEjec+=1
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                        
                        #aquí comienza el paso a paso
                        elif str(pasoaPaso) == 'pasoapaso' or str(sgtPaso) == 'sgtpaso' or str(sgtPaso) == 'fin' or varPrevPaP !='':
                            if str(pasoaPaso) == 'pasoapaso':
                                tempoLeer= colaP.pop() # se usa para tomar el ultimo proceso que llegó 
                                instanciaPaP.setLeer(leerLimp2) # se envia la lista con todas la lineas a paso a paso 
                                instanciaPaP.agregarInstrMemoria()
                            
                            rb = instanciaPaP.getRB() #se trae el registro base del programa en ejecución
                            rlc = instanciaPaP.getRLC() #se trae el registro límite de código del programa en ejecución
                            lineaParaIr= rb + contadorPasos
                            
                            global tieneQueLeerPaP
                            ###########################################
                            try:
                                lineaCod = leerLimp2[contadorPasos+1].split()
                                operando = lineaCod[0]
                            except :
                                lineaCod = ""
                                operando = ""
                            if operando == 'lea': 
                                varALeerPaP.append(lineaCod[1])
                                tieneQueLeerPaP = 1
                                print('entré aqui lea ', lineaCod[1])
                            ###########################################3

                            #tiene que leer tendra 3 estados, el primero activa ventana, el segundo toma los datos y el tercero envia los datos a pap
                            global ActivarVentLeerPaP

                            if tieneQueLeerPaP == 1: # tiene un lea para ingresar datos por teclado, activa la ventana donde se ingresan los datos
                                ActivarVentLeerPaP = True
                                tieneQueLeerPaP = 2
                                print('entré tiene que leer # 1')
                                
                                if contadorPasos == 0: #activa la ventana para poder ingresar los datos por teclado 
                                    
                                    print('este es el if', ' leer en pos cont en if 1.1', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                elif (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    
                                    else:
                                        contadorPasos += 1
                                
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 1.1', ' leer en pos cont', leerLimp2[contadorPasos])

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 
                                               

                            elif tieneQueLeerPaP ==2 : #lee lo que se está ingresando por teclado 

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = 3
                                instanciaPaP.setContinuarLeyendo(True)
                                print('entré tiene que leer # 2')

                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                               
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 



                                else:
                                    print('este es el else 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 
                                               


 

                            elif tieneQueLeerPaP ==3 : #se agregan los datos ingresando por teclado a el programa

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = -2
                                print('entré tiene que leer # 3')

                            
                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)
                                print(listaValoresVariTecladoPaP, 'supuestas variables de teclado')
                                instanciaPaP.setValoraLeer(listaValoresVariTecladoPaP)
                                instanciaPaP.setContinuarLeyendo(True)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                              
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


        ######################################################################################################################
                            else: # no tiene ningun lea para ingresar datos por teclado
                                instanciaPaP.setContinuarLeyendo(False)
                                print("esto es contador pasos", contadorPasos)
                                
                                if contadorPasos == 0:
                                    print('este es el if sin llamar leer 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 

                                elif str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc:
                                    print('este es el elif sin llamar leer 1.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    

                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                   

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        print("entre cambio curso", cambioCurso)
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 
                                                
                                else:
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos=0
                                    entro=0
                                    proEjec +=1
                                    print("ultimo paso sgte prog", proEjec)
                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos}) 
                        
                        else:
                            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione ejecutar o paso a paso para comenzar.'],'modo':'Modo kernel', 'continuarPaP':'True'}) # })#,   
            
            
    def get_object(self, queryset=None):
        
        profile, created= EjecArchCh.objects.get_or_create()
        return profile

class salirView(DeleteView):

    template_name = "core/delete.html"
    success_url= reverse_lazy('home')

    def get_object(self, queryset=None):
        global proEjec
        global entro
        global contadorPasos
        self.eliminaArchivos()
        deleteTodo = EjecArchCh.objects.all()
        proEjec = 0
        entro=-1
        contadorPasos=0
        return deleteTodo
    
    def eliminaArchivos(self):

        tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
        for tp in tup: 
            nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
            nombrActual = str(nombres)
            try:
                os.remove("media/" + nombrActual)
            except:
                print('no se ha eliminado el archivo')

## nuevas clases para los algoritmos de planificación de procesos
###########################################################################################################
class Calcular:
    @classmethod
    def tiempoLlegada(cls, cantIns, tAnterior):
        return (tAnterior + cantIns)/4
    
    @classmethod
    def Rafaga(cls, leer):#calcula las unidades de tiempo de rafaga que tiene cada proceso

        rafagaCPU =0
        rafagaIO=0
        io= ['lea','muestre','imprima']
        for lineas in leer:
            linea = lineas.rstrip().split()
            if linea[0] in io:
                rafagaIO += random.randint(1,9)
                #print(rafagaIO, 'io -ins', linea[0])
            else:
                rafagaCPU+=1
                #print(rafagaCPU,'cpu-ins', linea[0])
        
        return rafagaCPU+rafagaIO
        
    @classmethod
    def prioridad(cls):
        return random.randint(0,100)

    @classmethod
    def RafagaExprop(cls, leer):#calcula las unidades de tiempo de rafaga que tiene cada proceso

        rafagaCPU =0
        rafagaIO=0
        io= ['lea','muestre','imprima']
        for lineas in leer:
            #print(lineas, type(lineas))
            linea = lineas.rstrip().split()
            if linea[0] in io:

                temp= random.randint(1,9)
                dicTRafagaLinea[lineas]={'rafaga':temp, 'prog':proEjec} 
                rafagaIO += temp
                #print(rafagaIO, 'io -ins', linea[0])
            else:
                dicTRafagaLinea[lineas]={'rafaga':1, 'prog':proEjec} 
                rafagaCPU+=1
                #print(rafagaCPU,'cpu-ins', linea[0])
        
        print(dicTRafagaLinea)
        return rafagaCPU+rafagaIO
        



###############################################################################################    
class InicioPageView(TemplateView):#clase que muestra el listado de algoritmos en el front

    template_name = "core/inicio.html"
####################################################################################################################################33
#aqui comienza SPN version no expropiativa de SJF 
class SPNView(CreateView):
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('spn')
    template_name = "core/base.html"
    global cambioCurso
    global ActivarVentLeer
    global ActivarVentLeerPaP
    global varALeer
    global varALeerPaP
    global cuantosLea
    global cuantosLeaFaltan
    global tieneQueLeerPaP
    global proEjec
    global dicProc

    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self, leer,proEjec, cantmemoriaConKernel, cantMemoriaTotal, tamMemoriaConProg):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(leer)):
            palabras = leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if proEjec == 0:
            if cantmemoriaConKernel >= (len(leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (cantMemoriaTotal - tamMemoriaConProg) >= (len(leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def abrirArch(self, ruta):
        f="" #se utiliza para abrir el archivo desde la ruta relativa
        
        leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
        
        #aqui tratamos de leer el archivo si es posible.
        try:
            f = open("media/" + ruta, "r")
            leer = f.readlines() #para leer linea a linea
            f.close()
        except:
            print('no se puede abrir el archivo solicitado')  

        #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
        leerLimp=[] 
        for w in range(len(leer)):
            leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
        
        leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista

        return leerLimp2

    def procesoCorto(self,listaProcesos):
        #global proEjec
        listaKeys = list(listaProcesos.keys())
        masCorto = listaProcesos[listaKeys[0]] 
        numProc =0
        #print('mas corto---', masCorto)
        #print('esto es el diccionario',listaProcesos, '\n')  
        #print(listaProcesos[0]['tRafaga'],'listpro')
        
        for clave, valor in listaProcesos.items():   
            #print(listaProcesos[clave]['tRafaga'], '-trafaga de cada proceso')
            #print(masCorto['tRafaga'], 'mas corto')
            if listaProcesos[clave]['tRafaga'] < masCorto['tRafaga']: # compara los tiempos de rafaga 
                #print('aquí \n luego proEjec')
                #proEjec = clave
                numProc = clave
                #print(proEjec)
                masCorto = listaProcesos[clave]
            else:
                numProc = listaKeys[0]


        #print('el proceso mas corto es :', masCorto, '\n')
        return numProc

    def get(self, request, *args, **kwargs):
        global contadorPasos
        global cambioCurso
        global proEjec
        global entro
        leerLimp2=[] 
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
 

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione abir y cargue un archivo .ch, así, también cargará el tamaño de la memoria y el tamaño del kernel.'],'modo':'Modo kernel'}) # })#,   
           
        else:
            entro +=1
            print("esto es proEjec", proEjec)
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch
            pasoaPaso = request.GET.get('pasoapaso')
            sgtPaso = request.GET.get('sgtpaso')
            variablePorTeclado = request.GET.get('leaTeclado')
            variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
         
            nombre=""
            tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
            ruta=[]
            nombreArchivos=[]
            for tp in tup:

                nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                tempo2= str(nombres).split('/')
                nombreArchivos.append(tempo2[1])
                memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
            
                tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
            
            nombre=nombreArchivos[0] #nombre del archivo que se muestra en el front
            
            
            ##################################################################
            print('entro', entro,"\n")
            print(len(ruta), 'len de ruta')

            if entro <= len(ruta): #or contadorPasos==0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec-1]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
                print('se incrementa proEjc')
                proEjec +=1
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
            """
            listaprueba=[-1]*15
            print('\n','len 1', len(listaprueba))
            listaprueba[2] = '2'
            print(listaprueba.count(-1)-len(listaprueba))
            #listaprueba.insert(1,'k')
            #listaprueba.insert(0,'w')
            print('len 2', len(listaprueba),'\n')
            print('esto es lp',listaprueba)
            print('esto es lp',listaprueba[2])
            """

            """
            if entro == len(ruta) or contadorPasos>0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
                dicProc.clear()
                
            
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
               
                proEjec +=1
            """
            #print("cola inicio",colaP)
            #print("esto es spn")
            instanciaMemoria = memoria(int(memoriaTotal),int(kernelFinal))

            #############################################################################################################
            instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
            

            instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
            ###############################################################################################


            instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
            instanciaPaP = PaP() # se crea una instancia de la clase paso a paso para poder llamar los metodos necesarios para la ejecucion paso a paso

            if proEjec==0 and entro==1: # se necesita para cuando se sale del programa chmaquina y se vuelve a ingresar 
                instanciaEjec.clean()
                instanciaPaP.clean()
            
            #######################################################################
            instanciaEjec.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaEjec.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
           
            #instanciaEjec.setProgEjec(int(0)) # se envia el programa a ser ejecutado a la ejecución
            instanciaEjec.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ########################################################################
           
            
            ########################################################################
            instanciaPaP.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaPaP.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
            #instanciaPaP.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
            instanciaPaP.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ##########################################################################

            

            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el kernel con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
            
            else:
                #instanciaMemoria.agregarKernelMemoria() 07-06-2020
                instanciaEjec.agregarKernelMemoria()

                if contadorPasos ==0 and proEjec == 0 and not(cambioCurso):
                    instanciaPaP.agregarKernelMemoria()

                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                #if not(instanciaMemoria.puedeEjecProg()) and request.method == 'GET': 07-06-2020
                if not(self.puedeEjecProg(leerLimp2, proEjec,(memoriaTotal-kernelFinal),memoriaTotal,instanciaEjec.getTamMemoriaKernelProg())) and request.method == 'GET':
                #if not(instanciaEjec.puedeEjecProg()) and request.method == 'GET':
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el programa con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                else:
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                    else:
                        ######################################################
                        if request.GET.get('leaTeclado') == None:
                            varPrev = ""
                        else:
                            varPrev = request.GET.get('leaTeclado')
                        if request.GET.get('leaTecladoPaP') == None:
                            varPrevPaP = ""
                        else:
                            varPrevPaP = request.GET.get('leaTeclado')
                        ##############################################

                       
                        if str(ejecute) == 'ejecutarOk' or varPrev !='': 
                            
                            global varALeer
                            global varALeerPaP
                            global cuantosLea
                            global cuantosLeaFaltan
                            global listaValoresVariTeclado
                            global listaValoresVariTecladoPaP
                            lineaCod = ""
                            operando = ""

                            for i in range(len(leerLimp2)):
                                
                                try:
                                    lineaCod = leerLimp2[i].split()
                                    operando = lineaCod[0]
                                except :
                                    lineaCod = ""
                                    operando = ""
                                
                                if operando == 'lea': 
                                    varALeer.append(lineaCod[1])
                                    cuantosLea +=1 
                                
                            varALeer.reverse()
                            global ActivarVentLeer 
                         


                            if cuantosLeaFaltan == -1 and cuantosLea > 0 :
                                print('entré primer if')
                                cuantosLeaFaltan = cuantosLea
                                ActivarVentLeer = True 
                                cuantosLeaFaltan -=1

                                
                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':varALeer.pop()}) 
                                
                            elif varPrev !='' and cuantosLeaFaltan > 0:
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)
                                
                                if cuantosLeaFaltan > 0:
                                    ActivarVentLeer = True
                                    print('se volvio True')
                                else :
                                    print('se volvio false')
                                    ActivarVentLeer = False
                                cuantosLeaFaltan -=1

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                try:
                                    variable =varALeer.pop()
                                except:
                                    variable = "" 
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':variable}) 
                            
                            elif cuantosLeaFaltan == 0 :
                                ActivarVentLeer = False 
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)

                                instanciaEjec.setValoraLeer(listaValoresVariTeclado) ##despues de leer todos los valores
                                
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 

                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                            
                            #####################ejecución sin leer nada por teclado######################33
                            else:
                                #self.procesoCorto(dicProc)
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                #print(procesoSgte,'programa que se va a ejec','y esto es proceso sgte: ', procesoSgte)
                                ActivarVentLeer = False
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list)  
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                #proEjec+=1
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                        
                        #######################aquí comienza el paso a paso############################3
                        elif str(pasoaPaso) == 'pasoapaso' or str(sgtPaso) == 'sgtpaso' or str(sgtPaso) == 'fin' or varPrevPaP !='':
                            if str(pasoaPaso) == 'pasoapaso':
                               
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaPaP.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaPaP.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                
                                instanciaPaP.agregarInstrMemoria()
                            
                            rb = instanciaPaP.getRB() #se trae el registro base del programa en ejecución
                            rlc = instanciaPaP.getRLC() #se trae el registro límite de código del programa en ejecución
                            lineaParaIr= rb + contadorPasos
                            
                            global tieneQueLeerPaP
                            ###########################################
                            try:
                                lineaCod = leerLimp2[contadorPasos+1].split()
                                operando = lineaCod[0]
                            except :
                                lineaCod = ""
                                operando = ""
                            if operando == 'lea': 
                                varALeerPaP.append(lineaCod[1])
                                tieneQueLeerPaP = 1
                                print('entré aqui lea ', lineaCod[1])
                            ###########################################3

                            #tiene que leer tendra 3 estados, el primero activa ventana, el segundo toma los datos y el tercero envia los datos a pap
                            global ActivarVentLeerPaP

                            if tieneQueLeerPaP == 1: # tiene un lea para ingresar datos por teclado, activa la ventana donde se ingresan los datos
                                ActivarVentLeerPaP = True
                                tieneQueLeerPaP = 2
                                print('entré tiene que leer # 1')
                                
                                if contadorPasos == 0: #activa la ventana para poder ingresar los datos por teclado 
                                    
                                    print('este es el if', ' leer en pos cont en if 1.1', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                elif (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    
                                    else:
                                        contadorPasos += 1
                                
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 1.1', ' leer en pos cont', leerLimp2[contadorPasos])

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 
                                               

                            elif tieneQueLeerPaP ==2 : #lee lo que se está ingresando por teclado 

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = 3
                                instanciaPaP.setContinuarLeyendo(True)
                                print('entré tiene que leer # 2')

                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                               
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 



                                else:
                                    print('este es el else 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 
                                               

                            elif tieneQueLeerPaP ==3 : #se agregan los datos ingresando por teclado a el programa

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = -2
                                print('entré tiene que leer # 3')

                            
                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)
                                print(listaValoresVariTecladoPaP, 'supuestas variables de teclado')
                                instanciaPaP.setValoraLeer(listaValoresVariTecladoPaP)
                                instanciaPaP.setContinuarLeyendo(True)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                              
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


                                else:
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


    ######################################################################################################################
                            else: # no tiene ningun lea para ingresar datos por teclado
                                instanciaPaP.setContinuarLeyendo(False)
                                print("esto es contador pasos", contadorPasos)
                                
                                if contadorPasos == 0:
                                    print('este es el if sin llamar leer 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 

                                elif str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc:
                                    print('este es el elif sin llamar leer 1.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    

                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                   

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        print("entre cambio curso", cambioCurso)
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 
                                                
                                else:
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos=0
                                    entro=0
                                    
                                    print("ultimo paso sgte prog", proEjec)
                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos}) 
                        
                        else:
                            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione ejecutar o paso a paso para comenzar.'],'modo':'Modo kernel', 'continuarPaP':'True'}) # })#,   
            
            
    def get_object(self, queryset=None):
        
        profile, created= EjecArchCh.objects.get_or_create()
        return profile


############################################################################################################################3
#aquí comienza POR PRIORIDAD NO EXPROPIATIVO

class PrioridadNoExpView(CreateView):
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('prioridadNoExp')
    template_name = "core/base.html"
    global cambioCurso
    global ActivarVentLeer
    global ActivarVentLeerPaP
    global varALeer
    global varALeerPaP
    global cuantosLea
    global cuantosLeaFaltan
    global tieneQueLeerPaP
    global proEjec
    global dicProc

    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self, leer,proEjec, cantmemoriaConKernel, cantMemoriaTotal, tamMemoriaConProg):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(leer)):
            palabras = leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if proEjec == 0:
            if cantmemoriaConKernel >= (len(leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (cantMemoriaTotal - tamMemoriaConProg) >= (len(leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def abrirArch(self, ruta):
        f="" #se utiliza para abrir el archivo desde la ruta relativa
        
        leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
        
        #aqui tratamos de leer el archivo si es posible.
        try:
            f = open("media/" + ruta, "r")
            leer = f.readlines() #para leer linea a linea
            f.close()
        except:
            print('no se puede abrir el archivo solicitado')  

        #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
        leerLimp=[] 
        for w in range(len(leer)):
            leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
        
        leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista

        return leerLimp2

    def mayorPrioridad(self,listaProcesos):
        #global proEjec
        listaKeys = list(listaProcesos.keys())
        masCorto = listaProcesos[listaKeys[0]] 
        numProc =0
        #print('mas corto---', masCorto)
        #print('esto es el diccionario',listaProcesos, '\n')  
        #print(listaProcesos[0]['tRafaga'],'listpro')
        
        for clave, valor in listaProcesos.items():   
            #print(listaProcesos[clave]['tRafaga'], '-trafaga de cada proceso')
            #print(masCorto['tRafaga'], 'mas corto')
            if listaProcesos[clave]['tLlegada'] <= masCorto['tLlegada'] and listaProcesos[clave]['prioridad'] < masCorto['prioridad'] : # compara los tiempos de rafaga 
                #print('aquí \n luego proEjec')
                #proEjec = clave
                numProc = clave
                #print('numProc',numProc)
                masCorto = listaProcesos[clave]
            else:
                numProc = listaKeys[0]


        #print('el proceso mas corto es :', masCorto, '\n')
        return numProc

    def get(self, request, *args, **kwargs):
        global contadorPasos
        global cambioCurso
        global proEjec
        global entro
        leerLimp2=[] 
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
 

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione abir y cargue un archivo .ch, así, también cargará el tamaño de la memoria y el tamaño del kernel.'],'modo':'Modo kernel'}) # })#,   
           
        else:
            entro +=1
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch
            pasoaPaso = request.GET.get('pasoapaso')
            sgtPaso = request.GET.get('sgtpaso')
            variablePorTeclado = request.GET.get('leaTeclado')
            variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
         
            nombre=""
            tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
            ruta=[]
            nombreArchivos=[]
            for tp in tup:

                nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                tempo2= str(nombres).split('/')
                nombreArchivos.append(tempo2[1])
                memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
            
                tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
            
            nombre=nombreArchivos[0] #nombre del archivo que se muestra en el front
            
            
            ##################################################################
            print('entro', entro,"\n")
            

            if entro <= len(ruta): 
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                prioridad = Calcular.prioridad()
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec-1]['tLlegada'])
                print('tllegada', tLlegada)
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga, 'prioridad':prioridad} #guarda cada proceso con sus instrucciones, tiempo llegada, tiempo de rafaga y prioridad
                
                proEjec +=1
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)

            instanciaMemoria = memoria(int(memoriaTotal),int(kernelFinal))

            #############################################################################################################
            instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
            

            instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
            ###############################################################################################


            instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
            instanciaPaP = PaP() # se crea una instancia de la clase paso a paso para poder llamar los metodos necesarios para la ejecucion paso a paso

            if proEjec==0 and entro==1: # se necesita para cuando se sale del programa chmaquina y se vuelve a ingresar 
                instanciaEjec.clean()
                instanciaPaP.clean()
            
            #######################################################################
            instanciaEjec.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaEjec.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
           
            
            instanciaEjec.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ########################################################################
           
            
            ########################################################################
            instanciaPaP.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaPaP.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
            
            instanciaPaP.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ##########################################################################

            

            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el kernel con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
            
            else:
                
                instanciaEjec.agregarKernelMemoria()

                if contadorPasos ==0 and proEjec == 0 and not(cambioCurso):
                    instanciaPaP.agregarKernelMemoria()

                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                
                if not(self.puedeEjecProg(leerLimp2, proEjec,(memoriaTotal-kernelFinal),memoriaTotal,instanciaEjec.getTamMemoriaKernelProg())) and request.method == 'GET':
                
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el programa con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                else:
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                    else:
                        ######################################################
                        if request.GET.get('leaTeclado') == None:
                            varPrev = ""
                        else:
                            varPrev = request.GET.get('leaTeclado')
                        if request.GET.get('leaTecladoPaP') == None:
                            varPrevPaP = ""
                        else:
                            varPrevPaP = request.GET.get('leaTeclado')
                        ##############################################

                       
                        if str(ejecute) == 'ejecutarOk' or varPrev !='': 
                            
                            global varALeer
                            global varALeerPaP
                            global cuantosLea
                            global cuantosLeaFaltan
                            global listaValoresVariTeclado
                            global listaValoresVariTecladoPaP
                            lineaCod = ""
                            operando = ""

                            for i in range(len(leerLimp2)):
                                
                                try:
                                    lineaCod = leerLimp2[i].split()
                                    operando = lineaCod[0]
                                except :
                                    lineaCod = ""
                                    operando = ""
                                
                                if operando == 'lea': 
                                    varALeer.append(lineaCod[1])
                                    cuantosLea +=1 
                                
                            varALeer.reverse()
                            global ActivarVentLeer 
                         


                            if cuantosLeaFaltan == -1 and cuantosLea > 0 :
                                print('entré primer if')
                                cuantosLeaFaltan = cuantosLea
                                ActivarVentLeer = True 
                                cuantosLeaFaltan -=1

                                
                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':varALeer.pop()}) 
                                
                            elif varPrev !='' and cuantosLeaFaltan > 0:
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)
                                
                                if cuantosLeaFaltan > 0:
                                    ActivarVentLeer = True
                                    print('se volvio True')
                                else :
                                    print('se volvio false')
                                    ActivarVentLeer = False
                                cuantosLeaFaltan -=1

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                try:
                                    variable =varALeer.pop()
                                except:
                                    variable = "" 
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':variable}) 
                            
                            elif cuantosLeaFaltan == 0 :
                                ActivarVentLeer = False 
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)

                                instanciaEjec.setValoraLeer(listaValoresVariTeclado) ##despues de leer todos los valores
                                
                                procesoSgte = self.mayorPrioridad(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 

                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                            
                            #####################ejecución sin leer nada por teclado######################33
                            else:
                                #self.mayorPrioridad(dicProc)
                                procesoSgte = self.mayorPrioridad(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                #print(procesoSgte,'programa que se va a ejec','y esto es proceso sgte: ', procesoSgte)
                                ActivarVentLeer = False
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list)  
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                #proEjec+=1
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                        
                        #######################aquí comienza el paso a paso############################3
                        elif str(pasoaPaso) == 'pasoapaso' or str(sgtPaso) == 'sgtpaso' or str(sgtPaso) == 'fin' or varPrevPaP !='':
                            if str(pasoaPaso) == 'pasoapaso':
                               
                                procesoSgte = self.mayorPrioridad(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.mayorPrioridad(dicProc)  #dicProc.pop(0)
                                instanciaPaP.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaPaP.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                
                                instanciaPaP.agregarInstrMemoria()
                            
                            rb = instanciaPaP.getRB() #se trae el registro base del programa en ejecución
                            rlc = instanciaPaP.getRLC() #se trae el registro límite de código del programa en ejecución
                            lineaParaIr= rb + contadorPasos
                            
                            global tieneQueLeerPaP
                            ###########################################
                            try:
                                lineaCod = leerLimp2[contadorPasos+1].split()
                                operando = lineaCod[0]
                            except :
                                lineaCod = ""
                                operando = ""
                            if operando == 'lea': 
                                varALeerPaP.append(lineaCod[1])
                                tieneQueLeerPaP = 1
                                print('entré aqui lea ', lineaCod[1])
                            ###########################################3

                            #tiene que leer tendra 3 estados, el primero activa ventana, el segundo toma los datos y el tercero envia los datos a pap
                            global ActivarVentLeerPaP

                            if tieneQueLeerPaP == 1: # tiene un lea para ingresar datos por teclado, activa la ventana donde se ingresan los datos
                                ActivarVentLeerPaP = True
                                tieneQueLeerPaP = 2
                                print('entré tiene que leer # 1')
                                
                                if contadorPasos == 0: #activa la ventana para poder ingresar los datos por teclado 
                                    
                                    print('este es el if', ' leer en pos cont en if 1.1', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                elif (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    
                                    else:
                                        contadorPasos += 1
                                
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 1.1', ' leer en pos cont', leerLimp2[contadorPasos])

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 
                                               

                            elif tieneQueLeerPaP ==2 : #lee lo que se está ingresando por teclado 

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = 3
                                instanciaPaP.setContinuarLeyendo(True)
                                print('entré tiene que leer # 2')

                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                               
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 



                                else:
                                    print('este es el else 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 
                                               

                            elif tieneQueLeerPaP ==3 : #se agregan los datos ingresando por teclado a el programa

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = -2
                                print('entré tiene que leer # 3')

                            
                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)
                                print(listaValoresVariTecladoPaP, 'supuestas variables de teclado')
                                instanciaPaP.setValoraLeer(listaValoresVariTecladoPaP)
                                instanciaPaP.setContinuarLeyendo(True)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                              
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


                                else:
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


        ######################################################################################################################
                            else: # no tiene ningun lea para ingresar datos por teclado
                                instanciaPaP.setContinuarLeyendo(False)
                                print("esto es contador pasos", contadorPasos)
                                
                                if contadorPasos == 0:
                                    print('este es el if sin llamar leer 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 

                                elif str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc:
                                    print('este es el elif sin llamar leer 1.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    

                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                   

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        print("entre cambio curso", cambioCurso)
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 
                                                
                                else:
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos=0
                                    entro=0
                                    
                                    print("ultimo paso sgte prog", proEjec)
                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos}) 
                        
                        else:
                            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione ejecutar o paso a paso para comenzar.'],'modo':'Modo kernel', 'continuarPaP':'True'}) # })#,   
            
            
    def get_object(self, queryset=None):
        
        profile, created= EjecArchCh.objects.get_or_create()
        return profile


######################################################################################3
#aquí comienza SRTN

class SRTNView(CreateView):
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('srtn')
    template_name = "core/base.html"
    global cambioCurso
    global ActivarVentLeer
    global ActivarVentLeerPaP
    global varALeer
    global varALeerPaP
    global cuantosLea
    global cuantosLeaFaltan
    global tieneQueLeerPaP
    global proEjec
    global dicProc

    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self, leer,proEjec, cantmemoriaConKernel, cantMemoriaTotal, tamMemoriaConProg):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(leer)):
            palabras = leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if proEjec == 0:
            if cantmemoriaConKernel >= (len(leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (cantMemoriaTotal - tamMemoriaConProg) >= (len(leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def abrirArch(self, ruta):
        f="" #se utiliza para abrir el archivo desde la ruta relativa
        
        leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
        
        #aqui tratamos de leer el archivo si es posible.
        try:
            f = open("media/" + ruta, "r")
            leer = f.readlines() #para leer linea a linea
            f.close()
        except:
            print('no se puede abrir el archivo solicitado')  

        #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
        leerLimp=[] 
        for w in range(len(leer)):
            leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
        
        leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista

        return leerLimp2

    def procesoCorto(self,listaProcesos):
        #global proEjec
        listaKeys = list(listaProcesos.keys())
        masCorto = listaProcesos[listaKeys[0]] 
        numProc =0
        #print('mas corto---', masCorto)
        #print('esto es el diccionario',listaProcesos, '\n')  
        #print(listaProcesos[0]['tRafaga'],'listpro')
        
        for clave, valor in listaProcesos.items():   
            print(listaProcesos[clave]['tRafaga'], '-trafaga de cada proceso')
            print(listaProcesos[clave]['tLlegada'], '-tllegada de cada proceso')
            print(masCorto['tRafaga'], 'mas corto')
            if listaProcesos[clave]['tRafaga'] < masCorto['tRafaga']: # compara los tiempos de rafaga 
                #print('aquí \n luego proEjec')
                #proEjec = clave
                numProc = clave
                #print(proEjec)
                masCorto = listaProcesos[clave]
            else:
                numProc = listaKeys[0]


        #print('el proceso mas corto es :', masCorto, '\n')
        return numProc

    def get(self, request, *args, **kwargs):
        global contadorPasos
        global cambioCurso
        global proEjec
        global entro
        leerLimp2=[] 
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
 

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione abir y cargue un archivo .ch, así, también cargará el tamaño de la memoria y el tamaño del kernel.'],'modo':'Modo kernel'}) # })#,   
           
        else:
            entro +=1
            print("esto es proEjec", proEjec)
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch
            pasoaPaso = request.GET.get('pasoapaso')
            sgtPaso = request.GET.get('sgtpaso')
            variablePorTeclado = request.GET.get('leaTeclado')
            variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
         
            nombre=""
            tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
            ruta=[]
            nombreArchivos=[]
            for tp in tup:

                nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                tempo2= str(nombres).split('/')
                nombreArchivos.append(tempo2[1])
                memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
            
                tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
            
            nombre=nombreArchivos[0] #nombre del archivo que se muestra en el front
            
            
            ##################################################################
            print('entro', entro,"\n")
            print(len(ruta), 'len de ruta')

            if entro <= len(ruta): #or contadorPasos==0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec-1]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
                print('se incrementa proEjc')
                proEjec +=1
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
            """
            listaprueba=[-1]*15
            print('\n','len 1', len(listaprueba))
            listaprueba[2] = '2'
            print(listaprueba.count(-1)-len(listaprueba))
            #listaprueba.insert(1,'k')
            #listaprueba.insert(0,'w')
            print('len 2', len(listaprueba),'\n')
            print('esto es lp',listaprueba)
            print('esto es lp',listaprueba[2])
            """

            """
            if entro == len(ruta) or contadorPasos>0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
                dicProc.clear()
                
            
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
               
                proEjec +=1
            """
            #print("cola inicio",colaP)
            #print("esto es spn")
            instanciaMemoria = memoria(int(memoriaTotal),int(kernelFinal))

            #############################################################################################################
            instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
            

            instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
            ###############################################################################################


            instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
            instanciaPaP = PaP() # se crea una instancia de la clase paso a paso para poder llamar los metodos necesarios para la ejecucion paso a paso

            if proEjec==0 and entro==1: # se necesita para cuando se sale del programa chmaquina y se vuelve a ingresar 
                instanciaEjec.clean()
                instanciaPaP.clean()
            
            #######################################################################
            instanciaEjec.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaEjec.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
           
            #instanciaEjec.setProgEjec(int(0)) # se envia el programa a ser ejecutado a la ejecución
            instanciaEjec.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ########################################################################
           
            
            ########################################################################
            instanciaPaP.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaPaP.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
            #instanciaPaP.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
            instanciaPaP.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ##########################################################################

            

            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el kernel con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
            
            else:
                #instanciaMemoria.agregarKernelMemoria() 07-06-2020
                instanciaEjec.agregarKernelMemoria()

                if contadorPasos ==0 and proEjec == 0 and not(cambioCurso):
                    instanciaPaP.agregarKernelMemoria()

                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                #if not(instanciaMemoria.puedeEjecProg()) and request.method == 'GET': 07-06-2020
                if not(self.puedeEjecProg(leerLimp2, proEjec,(memoriaTotal-kernelFinal),memoriaTotal,instanciaEjec.getTamMemoriaKernelProg())) and request.method == 'GET':
                #if not(instanciaEjec.puedeEjecProg()) and request.method == 'GET':
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el programa con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                else:
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                    else:
                        ######################################################
                        if request.GET.get('leaTeclado') == None:
                            varPrev = ""
                        else:
                            varPrev = request.GET.get('leaTeclado')
                        if request.GET.get('leaTecladoPaP') == None:
                            varPrevPaP = ""
                        else:
                            varPrevPaP = request.GET.get('leaTeclado')
                        ##############################################

                       
                        if str(ejecute) == 'ejecutarOk' or varPrev !='': 
                            
                            global varALeer
                            global varALeerPaP
                            global cuantosLea
                            global cuantosLeaFaltan
                            global listaValoresVariTeclado
                            global listaValoresVariTecladoPaP
                            lineaCod = ""
                            operando = ""

                            for i in range(len(leerLimp2)):
                                
                                try:
                                    lineaCod = leerLimp2[i].split()
                                    operando = lineaCod[0]
                                except :
                                    lineaCod = ""
                                    operando = ""
                                
                                if operando == 'lea': 
                                    varALeer.append(lineaCod[1])
                                    cuantosLea +=1 
                                
                            varALeer.reverse()
                            global ActivarVentLeer 
                         


                            if cuantosLeaFaltan == -1 and cuantosLea > 0 :
                                print('entré primer if')
                                cuantosLeaFaltan = cuantosLea
                                ActivarVentLeer = True 
                                cuantosLeaFaltan -=1

                                
                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':varALeer.pop()}) 
                                
                            elif varPrev !='' and cuantosLeaFaltan > 0:
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)
                                
                                if cuantosLeaFaltan > 0:
                                    ActivarVentLeer = True
                                    print('se volvio True')
                                else :
                                    print('se volvio false')
                                    ActivarVentLeer = False
                                cuantosLeaFaltan -=1

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                try:
                                    variable =varALeer.pop()
                                except:
                                    variable = "" 
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':variable}) 
                            
                            elif cuantosLeaFaltan == 0 :
                                ActivarVentLeer = False 
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)

                                instanciaEjec.setValoraLeer(listaValoresVariTeclado) ##despues de leer todos los valores
                                
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 

                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                            
                            #####################ejecución sin leer nada por teclado######################33
                            else:
                                #self.procesoCorto(dicProc)
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                #print(procesoSgte,'programa que se va a ejec','y esto es proceso sgte: ', procesoSgte)
                                ActivarVentLeer = False
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list)  
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                #proEjec+=1
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                        
                        #######################aquí comienza el paso a paso############################3
                        elif str(pasoaPaso) == 'pasoapaso' or str(sgtPaso) == 'sgtpaso' or str(sgtPaso) == 'fin' or varPrevPaP !='':
                            if str(pasoaPaso) == 'pasoapaso':
                               
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaPaP.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaPaP.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                
                                instanciaPaP.agregarInstrMemoria()
                            
                            rb = instanciaPaP.getRB() #se trae el registro base del programa en ejecución
                            rlc = instanciaPaP.getRLC() #se trae el registro límite de código del programa en ejecución
                            lineaParaIr= rb + contadorPasos
                            
                            global tieneQueLeerPaP
                            ###########################################
                            try:
                                lineaCod = leerLimp2[contadorPasos+1].split()
                                operando = lineaCod[0]
                            except :
                                lineaCod = ""
                                operando = ""
                            if operando == 'lea': 
                                varALeerPaP.append(lineaCod[1])
                                tieneQueLeerPaP = 1
                                print('entré aqui lea ', lineaCod[1])
                            ###########################################3

                            #tiene que leer tendra 3 estados, el primero activa ventana, el segundo toma los datos y el tercero envia los datos a pap
                            global ActivarVentLeerPaP

                            if tieneQueLeerPaP == 1: # tiene un lea para ingresar datos por teclado, activa la ventana donde se ingresan los datos
                                ActivarVentLeerPaP = True
                                tieneQueLeerPaP = 2
                                print('entré tiene que leer # 1')
                                
                                if contadorPasos == 0: #activa la ventana para poder ingresar los datos por teclado 
                                    
                                    print('este es el if', ' leer en pos cont en if 1.1', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                elif (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    
                                    else:
                                        contadorPasos += 1
                                
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 1.1', ' leer en pos cont', leerLimp2[contadorPasos])

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 
                                               

                            elif tieneQueLeerPaP ==2 : #lee lo que se está ingresando por teclado 

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = 3
                                instanciaPaP.setContinuarLeyendo(True)
                                print('entré tiene que leer # 2')

                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                               
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 



                                else:
                                    print('este es el else 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 
                                               

                            elif tieneQueLeerPaP ==3 : #se agregan los datos ingresando por teclado a el programa

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = -2
                                print('entré tiene que leer # 3')

                            
                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)
                                print(listaValoresVariTecladoPaP, 'supuestas variables de teclado')
                                instanciaPaP.setValoraLeer(listaValoresVariTecladoPaP)
                                instanciaPaP.setContinuarLeyendo(True)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                              
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


                                else:
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


    ######################################################################################################################
                            else: # no tiene ningun lea para ingresar datos por teclado
                                instanciaPaP.setContinuarLeyendo(False)
                                print("esto es contador pasos", contadorPasos)
                                
                                if contadorPasos == 0:
                                    print('este es el if sin llamar leer 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 

                                elif str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc:
                                    print('este es el elif sin llamar leer 1.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    

                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                   

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        print("entre cambio curso", cambioCurso)
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 
                                                
                                else:
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos=0
                                    entro=0
                                    
                                    print("ultimo paso sgte prog", proEjec)
                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos}) 
                        
                        else:
                            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione ejecutar o paso a paso para comenzar.'],'modo':'Modo kernel', 'continuarPaP':'True'}) # })#,   
            
            
    def get_object(self, queryset=None):
        
        profile, created= EjecArchCh.objects.get_or_create()
        return profile



###########################################################################################
#aquí comienza Round Robin 

class RRView(CreateView):
    model = EjecArchCh
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('rr')
    template_name = "core/base.html"
    global cambioCurso
    global ActivarVentLeer
    global ActivarVentLeerPaP
    global varALeer
    global varALeerPaP
    global cuantosLea
    global cuantosLeaFaltan
    global tieneQueLeerPaP
    global proEjec
    global dicProc

    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self, leer,proEjec, cantmemoriaConKernel, cantMemoriaTotal, tamMemoriaConProg):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(leer)):
            palabras = leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if proEjec == 0:
            if cantmemoriaConKernel >= (len(leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (cantMemoriaTotal - tamMemoriaConProg) >= (len(leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def abrirArch(self, ruta):
        f="" #se utiliza para abrir el archivo desde la ruta relativa
        
        leer=[] # aquí se guardan todas las instrucciones del archivo .ch 
        
        #aqui tratamos de leer el archivo si es posible.
        try:
            f = open("media/" + ruta, "r")
            leer = f.readlines() #para leer linea a linea
            f.close()
        except:
            print('no se puede abrir el archivo solicitado')  

        #aquí se retiran el \n que adiciona python cuando lee un archivo de texto
        leerLimp=[] 
        for w in range(len(leer)):
            leerLimp.append(leer[w].rstrip()) #se deja el archivo sin el salto de linea que agrega python
        
        leerLimp2=[i for i in leerLimp if i != ''] # se utiliza para quitar los espacios vacios que pueda tener la lista

        return leerLimp2

    def procesoCorto(self,listaProcesos):
        #global proEjec
        listaKeys = list(listaProcesos.keys())
        masCorto = listaProcesos[listaKeys[0]] 
        numProc =0
        #print('mas corto---', masCorto)
        #print('esto es el diccionario',listaProcesos, '\n')  
        #print(listaProcesos[0]['tRafaga'],'listpro')
        
        for clave, valor in listaProcesos.items():   
            print(listaProcesos[clave]['tRafaga'], '-trafaga de cada proceso')
            print(listaProcesos[clave]['tLlegada'], '-tllegada de cada proceso')
            print(masCorto['tRafaga'], 'mas corto')
            if listaProcesos[clave]['tRafaga'] < masCorto['tRafaga']: # compara los tiempos de rafaga 
                #print('aquí \n luego proEjec')
                #proEjec = clave
                numProc = clave
                #print(proEjec)
                masCorto = listaProcesos[clave]
            else:
                numProc = listaKeys[0]


        #print('el proceso mas corto es :', masCorto, '\n')
        return numProc

    def get(self, request, *args, **kwargs):
        global contadorPasos
        global cambioCurso
        global proEjec
        global entro
        leerLimp2=[] 
        ejecute = request.GET.get('ejecute') # se toma lo que se envia a través de una peticion ajax 
 

        tup = EjecArchCh.objects.all()
        if not(tup): # cuando la base de datos se encuentra vacia 
            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione abir y cargue un archivo .ch, así, también cargará el tamaño de la memoria y el tamaño del kernel.'],'modo':'Modo kernel'}) # })#,   
           
        else:
            entro +=1
            print("esto es proEjec", proEjec)
            ejecute = request.GET.get('ejecute') # se utliza este metodo para tomar la peticion ajax realizada desde el front para ejecutar un archivo .ch
            pasoaPaso = request.GET.get('pasoapaso')
            sgtPaso = request.GET.get('sgtpaso')
            variablePorTeclado = request.GET.get('leaTeclado')
            variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
         
            nombre=""
            tup = EjecArchCh.objects.all() # aquí se toman los datos desde la base de datos 
            ruta=[]
            nombreArchivos=[]
            for tp in tup:

                nombres=tp.archivo # aquí se toman todas la rutas de los archivos cargados en la bd
                ruta.append(str(nombres)) # se toman todo las rutas relativas de la base de datos
                memorias= tp.memoria # aquí se toman las cantidades de memoria guardadas en la bd
                kernels=tp.kernel # aquí se toman las cantidades de kernel guardadas en la bd
                tempo2= str(nombres).split('/')
                nombreArchivos.append(tempo2[1])
                memoriaTotal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
                kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
            
                tamMemoriaDisp = memoriaTotal- kernelFinal -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
                cantidadKernel=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
                cantidMemoriaDisp=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
            
            nombre=nombreArchivos[0] #nombre del archivo que se muestra en el front
            
            
            ##################################################################
            print('entro', entro,"\n")
            print(len(ruta), 'len de ruta')

            if entro <= len(ruta): #or contadorPasos==0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.RafagaExprop(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec-1]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
                print('se incrementa proEjc')
                proEjec +=1
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
            """
            listaprueba=[-1]*15
            print('\n','len 1', len(listaprueba))
            listaprueba[2] = '2'
            print(listaprueba.count(-1)-len(listaprueba))
            #listaprueba.insert(1,'k')
            #listaprueba.insert(0,'w')
            print('len 2', len(listaprueba),'\n')
            print('esto es lp',listaprueba)
            print('esto es lp',listaprueba[2])
            """

            """
            if entro == len(ruta) or contadorPasos>0:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                leerLimp2= self.abrirArch(rutaPrograma)
                dicProc.clear()
                
            
            else:
                rutaPrograma =""
                try:
                    rutaPrograma =ruta[proEjec]
                except:
                    rutaPrograma =ruta[0]
                    print("error en la ruta del último programa")
                
                leerLimp2= self.abrirArch(rutaPrograma)
                tLlegada = 0
                tRafaga= Calcular.Rafaga(leerLimp2)
                if proEjec ==0:
                    tLlegada = 0
                else:
                    tLlegada = Calcular.tiempoLlegada(len(leerLimp2),dicProc[proEjec]['tLlegada'])
                
                dicProc[proEjec]= {'leer':leerLimp2,'tLlegada':tLlegada,'tRafaga':tRafaga} #guarda cada proceso con sus instrucciones, tiempo llegada y tiempo de rafaga
               
                proEjec +=1
            """
            #print("cola inicio",colaP)
            #print("esto es spn")
            instanciaMemoria = memoria(int(memoriaTotal),int(kernelFinal))

            #############################################################################################################
            instanciaSintaxis= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
            

            instanciaSintaxis.setLeer(leerLimp2) # se envia la lista con todas la lineas a sintaxis 
            ###############################################################################################


            instanciaEjec = ejecucion() # se crea una instancia de la clase ejecucion para poder llamar los metodos necesarios para la ejecucion
            instanciaPaP = PaP() # se crea una instancia de la clase paso a paso para poder llamar los metodos necesarios para la ejecucion paso a paso

            if proEjec==0 and entro==1: # se necesita para cuando se sale del programa chmaquina y se vuelve a ingresar 
                instanciaEjec.clean()
                instanciaPaP.clean()
            
            #######################################################################
            instanciaEjec.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaEjec.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
           
            #instanciaEjec.setProgEjec(int(0)) # se envia el programa a ser ejecutado a la ejecución
            instanciaEjec.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ########################################################################
           
            
            ########################################################################
            instanciaPaP.setCantMemo(int(memoriaTotal)) # se envia la cantidad de memoria a la ejecución
            instanciaPaP.setKernel(int(kernelFinal)) # se envia la cantidad de kernel a la ejecución
            #instanciaPaP.setProgEjec(int(proEjec)) # se envia el programa a ser ejecutado a la ejecución
            instanciaPaP.setRuta(ruta) # se envia las rutas de los archivos a la ejecución
            ##########################################################################

            

            if not(instanciaEjec.puedeEjecKernel()):
                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+1) #NO PUEDE AGREGAR KERNEL se pone la memoria total disponible
                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el kernel con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal, 'modo':'Modo kernel'}) # })#,   
            
            else:
                #instanciaMemoria.agregarKernelMemoria() 07-06-2020
                instanciaEjec.agregarKernelMemoria()

                if contadorPasos ==0 and proEjec == 0 and not(cambioCurso):
                    instanciaPaP.agregarKernelMemoria()

                for i in range (tamMemoriaDisp): #aqui se llena la lista con los valores de la posicion de memoria disponible
                    cantidMemoriaDisp.append(i+kernelFinal+1) # PUEDE AGREGAR KERNEL PERO NO PUEDE EJECUTAR
                for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
                    cantidadKernel.append(i+1) 

                #if not(instanciaMemoria.puedeEjecProg()) and request.method == 'GET': 07-06-2020
                if not(self.puedeEjecProg(leerLimp2, proEjec,(memoriaTotal-kernelFinal),memoriaTotal,instanciaEjec.getTamMemoriaKernelProg())) and request.method == 'GET':
                #if not(instanciaEjec.puedeEjecProg()) and request.method == 'GET':
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':['No hay suficiente espacio para el programa con respecto al tamaño de la memoria.'],'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel, 'memoriaTotal':memoriaTotal,'modo':'Modo kernel'}) # })#,

                else:
                    instanciaSintaxis.errSintax() # con esto se llama la funcion donde se verifica cada linea y se entrega en que linea se encuentra el error si lo hay
                    if instanciaSintaxis.hayError():  
                        ## se mostraría el error que tiene el programa .ch
                        return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':instanciaSintaxis.getPantalla(),'memoriaDis': cantidMemoriaDisp, 'kernel': kernelFinal, 'memKer':cantidadKernel,'memoriaTotal':memoriaTotal, 'modo':'Modo kernel',}) # })#, cantidadKernel (lista con las posiciones de kernel)

                    else:
                        ######################################################
                        if request.GET.get('leaTeclado') == None:
                            varPrev = ""
                        else:
                            varPrev = request.GET.get('leaTeclado')
                        if request.GET.get('leaTecladoPaP') == None:
                            varPrevPaP = ""
                        else:
                            varPrevPaP = request.GET.get('leaTeclado')
                        ##############################################

                       
                        if str(ejecute) == 'ejecutarOk' or varPrev !='': 
                            
                            global varALeer
                            global varALeerPaP
                            global cuantosLea
                            global cuantosLeaFaltan
                            global listaValoresVariTeclado
                            global listaValoresVariTecladoPaP
                            lineaCod = ""
                            operando = ""

                            for i in range(len(leerLimp2)):
                                
                                try:
                                    lineaCod = leerLimp2[i].split()
                                    operando = lineaCod[0]
                                except :
                                    lineaCod = ""
                                    operando = ""
                                
                                if operando == 'lea': 
                                    varALeer.append(lineaCod[1])
                                    cuantosLea +=1 
                                
                            varALeer.reverse()
                            global ActivarVentLeer 
                         


                            if cuantosLeaFaltan == -1 and cuantosLea > 0 :
                                print('entré primer if')
                                cuantosLeaFaltan = cuantosLea
                                ActivarVentLeer = True 
                                cuantosLeaFaltan -=1

                                
                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':varALeer.pop()}) 
                                
                            elif varPrev !='' and cuantosLeaFaltan > 0:
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)
                                
                                if cuantosLeaFaltan > 0:
                                    ActivarVentLeer = True
                                    print('se volvio True')
                                else :
                                    print('se volvio false')
                                    ActivarVentLeer = False
                                cuantosLeaFaltan -=1

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                try:
                                    variable =varALeer.pop()
                                except:
                                    variable = "" 
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, 'varALeer':variable}) 
                            
                            elif cuantosLeaFaltan == 0 :
                                ActivarVentLeer = False 
                                
                                variablePorTeclado = request.GET.get('leaTeclado')
                                listaValoresVariTeclado.append(variablePorTeclado)

                                instanciaEjec.setValoraLeer(listaValoresVariTeclado) ##despues de leer todos los valores
                                
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list) 
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 

                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                            
                            #####################ejecución sin leer nada por teclado######################33
                            else:
                                #self.procesoCorto(dicProc)
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaEjec.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaEjec.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                #print(procesoSgte,'programa que se va a ejec','y esto es proceso sgte: ', procesoSgte)
                                ActivarVentLeer = False
                                instanciaEjec.agregarInstrMemoria() # agrega las instrucciones a la memoria
                                instanciaEjec.ejecutarProg(-2) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal

                                pant = instanciaEjec.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                impre = instanciaEjec.getImpresora() # (str) datos impresora en el frontend
                                acum = instanciaEjec.getAcumulador() # (str) 
                                linAct = instanciaEjec.getLineaActual() # (str) 
                                codProAct = instanciaEjec.getCodProgActual() # (list) 
                                varAct = instanciaEjec.getVariablesActuales()# (list)  
                                etiqAct = instanciaEjec.getEtiquetasActuales() # (list) 
                                mem = instanciaEjec.getMemoria() # (list) 
                                prog = instanciaEjec.getProgramas() # (list) 
                                memDis = instanciaEjec.getMemoriaDispo() # (list) 
                                #proEjec+=1
                                return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog,'actiModal':ActivarVentLeer, }) 
                        
                        #######################aquí comienza el paso a paso############################3
                        elif str(pasoaPaso) == 'pasoapaso' or str(sgtPaso) == 'sgtpaso' or str(sgtPaso) == 'fin' or varPrevPaP !='':
                            if str(pasoaPaso) == 'pasoapaso':
                               
                                procesoSgte = self.procesoCorto(dicProc)
                                temporal = dicProc.pop(procesoSgte) #self.procesoCorto(dicProc)  #dicProc.pop(0)
                                instanciaPaP.setProgEjec(procesoSgte) # se envia el programa a ser ejecutado a la ejecución
                                
                                instanciaPaP.setLeer(temporal['leer']) # se envia la lista con todas la lineas a ejecucion 
                                
                                
                                instanciaPaP.agregarInstrMemoria()
                            
                            rb = instanciaPaP.getRB() #se trae el registro base del programa en ejecución
                            rlc = instanciaPaP.getRLC() #se trae el registro límite de código del programa en ejecución
                            lineaParaIr= rb + contadorPasos
                            
                            global tieneQueLeerPaP
                            ###########################################
                            try:
                                lineaCod = leerLimp2[contadorPasos+1].split()
                                operando = lineaCod[0]
                            except :
                                lineaCod = ""
                                operando = ""
                            if operando == 'lea': 
                                varALeerPaP.append(lineaCod[1])
                                tieneQueLeerPaP = 1
                                print('entré aqui lea ', lineaCod[1])
                            ###########################################3

                            #tiene que leer tendra 3 estados, el primero activa ventana, el segundo toma los datos y el tercero envia los datos a pap
                            global ActivarVentLeerPaP

                            if tieneQueLeerPaP == 1: # tiene un lea para ingresar datos por teclado, activa la ventana donde se ingresan los datos
                                ActivarVentLeerPaP = True
                                tieneQueLeerPaP = 2
                                print('entré tiene que leer # 1')
                                
                                if contadorPasos == 0: #activa la ventana para poder ingresar los datos por teclado 
                                    
                                    print('este es el if', ' leer en pos cont en if 1.1', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                elif (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    
                                    else:
                                        contadorPasos += 1
                                
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 



                                else:
                                    print('este es el else 1.1', ' leer en pos cont', leerLimp2[contadorPasos])

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 
                                               

                            elif tieneQueLeerPaP ==2 : #lee lo que se está ingresando por teclado 

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = 3
                                instanciaPaP.setContinuarLeyendo(True)
                                print('entré tiene que leer # 2')

                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el elif 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                               
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 



                                else:
                                    print('este es el else 2.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP, 'varALeerPaP':varALeerPaP.pop()}) 
                                               

                            elif tieneQueLeerPaP ==3 : #se agregan los datos ingresando por teclado a el programa

                                ActivarVentLeerPaP = False
                                tieneQueLeerPaP = -2
                                print('entré tiene que leer # 3')

                            
                                variablePorTecladoPaP = request.GET.get('leaTecladoPaP')
                                listaValoresVariTecladoPaP.append(variablePorTecladoPaP)
                                print(listaValoresVariTecladoPaP, 'supuestas variables de teclado')
                                instanciaPaP.setValoraLeer(listaValoresVariTecladoPaP)
                                instanciaPaP.setContinuarLeyendo(True)

                                if (str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc) or (varPrevPaP != '' and lineaParaIr < rlc):
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                              
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


                                else:
                                    print('este es el else 3.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos+=1

                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos, 'actiModalPaP': ActivarVentLeerPaP}) 


    ######################################################################################################################
                            else: # no tiene ningun lea para ingresar datos por teclado
                                instanciaPaP.setContinuarLeyendo(False)
                                print("esto es contador pasos", contadorPasos)
                                
                                if contadorPasos == 0:
                                    print('este es el if sin llamar leer 1.1', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(rb) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    
                                    cambioCurso = instanciaPaP.getCambiaCurso()

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1
                                    
                                    
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 

                                elif str(sgtPaso) == 'sgtpaso' and lineaParaIr < rlc:
                                    print('este es el elif sin llamar leer 1.2', ' leer en pos cont', leerLimp2[contadorPasos])
                                    instanciaPaP.ejecutarProgPaP(lineaParaIr) # se agrega un valor negativo puesto que no es necesario este parametro para una ejecución normal
                                    

                                    cambioCurso = instanciaPaP.getCambiaCurso()
                                   

                                    if cambioCurso:#(operando == 'vayasi' or operando == 'vaya') and cambioCurso:
                                        print("entre cambio curso", cambioCurso)
                                        contadorPasos = instanciaPaP.getPosaCambiar() - rb
                                        cambioCurso=False
                                        instanciaPaP.setCambiaCurso(False)
                                    else:
                                        contadorPasos += 1

                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     



                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'True', 'sgtpaso':'sgtpaso', 'contadorPasos':contadorPasos}) 
                                                
                                else:
                                    pant = instanciaPaP.getPantalla() #datos enviados para mostrar en la pantalla desde ejecucion
                                    impre = instanciaPaP.getImpresora() # (str) datos impresora en el frontend
                                    acum = instanciaPaP.getAcumulador() # (str) 
                                    linAct = instanciaPaP.getLineaActual() # (str) 
                                    codProAct = instanciaPaP.getCodProgActual() # (list) 
                                    varAct = instanciaPaP.getVariablesActuales()# (list) 
                                    etiqAct = instanciaPaP.getEtiquetasActuales() # (list) 
                                    mem = instanciaPaP.getMemoria() # (list) 
                                    prog = instanciaPaP.getProgramas() # (list) 
                                    memDis = instanciaPaP.getMemoriaDispo() # (list)     

                                    contadorPasos=0
                                    entro=0
                                    
                                    print("ultimo paso sgte prog", proEjec)
                                    return render(request, self.template_name,{'title': "Ch Máquina",'nombre':nombre, 'pantallaBack':pant ,'memoriaDis': memDis, 'kernel': kernelFinal, 'memoriaTotal':memoriaTotal,
                                                    'impre': impre, 'acum': acum, 'linAct': linAct,  'codProAct': codProAct, 'varAct': varAct,
                                                    'etiqAct': etiqAct,'mem':mem, 'modo':'Modo usuario', 'prog':prog, 'continuarPaP':'False', 'sgtpaso':'fin', 'contadorPasos':contadorPasos}) 
                        
                        else:
                            return render(request, self.template_name,{'title': "Ch Máquina",'pantallaBack':['Presione ejecutar o paso a paso para comenzar.'],'modo':'Modo kernel', 'continuarPaP':'True'}) # })#,   
            
            
    def get_object(self, queryset=None):
        
        profile, created= EjecArchCh.objects.get_or_create()
        return profile

