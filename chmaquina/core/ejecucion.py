from django.core.files import File
import threading
import time

activarVentLeer = True # se enviará al front para mostrar una ventana donde se leen los datos de las var
valoresLeidos=[] #valor traido desde el front para la funcion leer
class ejecucion:

    cantmemoria= 0 
    cantidadFull = 0 #cantidad full de memoria
    kernel= 0
    proEjec=0 # id del programa que se ejecuta actualmente
    leer=[] # todas las lineas del codigo del programa .ch
    ruta2=[] # todos los programas que estan en la bd

    # necesasario para quitar el \n que se genera en algunos archivos .ch
    contraS =[]
    contadorSalto=0 # contador de salto de linea
    i=0
    for i in range(len(leer)):
        contraS = leer[i] # variable para verificar si hay un salto de linea
        if contraS == str('\n'):
            contadorSalto +=1
    j=0
    for j in range(contadorSalto):
        leer.remove(str('\n'))

    
    #estructuras de datos necesarias (se contempla leer[] y ruta2[]=>que es la lista de programas(los nombres)).
    memoria =[] # memoria donde se guarda el kernel, los programas y el acumulador
    variables =[] #aqui se guardan los nombres de las variables
    posMemVar=[]
    cantidVarixPro=[0]*30 # aqui se sabe cuantas variables son agregadas en cada uno de los programas, que representan una posicion en el arreglo 
    etiquetas =[] #aqui se guardan los nombres de la etiquetas
    posMemEtiq=[]
    memoria.append(0) # memoria en la primera posición será el acumudador (variable requerida en el ch máquina)
    cantmemoria -= 1 # aqui se disminuye en 1 cuando se toma el acumulador 
    rb=[] # registro base del programa, donde empieza el programa, cada posicion corresponde a un programa (ejem rb[0] es el rb del programa 0)
    rlc =[] # registro limite del codigo, hasta donde llegan las instrucciones del programa, cada posicion corresponde a un programa (ejem rlc[0] es el rlc del programa 0) 
    rlp=[] # registro limite del programa, hasta donde llega el programa, con variables incluidas, cada posicion corresponde a un programa (ejem rlp[0] es el rlp del programa 0)
    pantalla =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    impresora =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    
    global valoresLeidos
    
    stopH=False # variable para detener ejecucion del hilo ppal
    global activarVentLeer

    ###############################################################################
    # necesasario para quitar el \n que se genera en algunos archivos .ch
    contadorSalto=0 # contador de salto de linea
    contadorVacio =0
    i=0
    contraS=""
    w=0
    for w in range(len(leer)):  
        contraS = leer[w] # variable para verificar si hay un salto de linea
        if contraS == str('\n'):
            contadorSalto +=1
        elif contraS == '' :
            contadorVacio +=1
            print(contadorVacio) 
    j=0
    for j in range(contadorVacio):
        leer.remove('')

    j=0
    for j in range(contadorSalto):
        leer.remove(str('\n'))
    ################################################################################

    ########## metodos para traer los datos de la bd necesarios para la ejecucion del archivo ###################
    def setKernel(self, kernel): # introduce cantidad de memoria del programa en ejecucion
        self.kernel=kernel

    def setCantMemo(self, cantidMemo):  # introduce la cantidad de memoria del programa en ejecucion 
        if self.proEjec == 0:
            self.cantmemoria=cantidMemo
            self.cantidadFull = cantidMemo
        else:
            print('cantidad memoria else' + self.cantmemoria)
 
    def setLeer(self, leer): # introduce todas las lineas del archivo .ch
        self.leer = leer
    
    def setProgEjec(self, progEjec): # introduce el programa en ejecucion 
        self.proEjec = progEjec
    
    def setRuta(self, ruta): # introduce la lista de programas en la bd 
        self.ruta2 = ruta

    #introduce las variables por teclado
    def setValoraLeer(self, valorVariables):
        global valoresLeidos
        valoresLeidos = valorVariables

    #entrega en el front si se debe seguir desplegando la ventana modal de lectura
    def getActivarVentLeer(self):
        global activarVentLeer
        return activarVentLeer
    
    def setActivarVentLeer(self, activo):
        global activarVentLeer
        activarVentLeer = activo

    def playHppal(self):#inicia el hilo principal de ejecucion
        vlrIni = "-2"
        hilo = threading.Thread(target=self.ejecutarProg, args=("-2",))
        hilo.start()

    def stopHppal(self):
        self.stopH = True
    #####################################################################################


    # metodo que comprueba si es posible realizar la ejecución (la memoria debe ser mayor al kernel)
    def puedeEjecKernel(self):
        #if cantidMemo > kernel:
        if self.cantmemoria > self.kernel:
            self.cantmemoria -= self.kernel 
            return True
        else:
            return False #se mostraria un error en la pantalla 
    
    # metodo que comprueba si es posible realizar la ejecución (la memoria disponible debe ser mayor que el programa a cargar)
    def puedeEjecProg(self):
        posiblesVar = 0 # se utiliza para verificar cuantas variables se crean en el programa 

        for i in range(len(self.leer)):
            palabras = self.leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if self.proEjec == 0:
            if self.cantmemoria >= (len(self.leer)+posiblesVar): 
                return True
            else:
                return False #se mostraria un error en la pantalla 
        else:
            if (self.cantidadFull - len(self.memoria)) >= (len(self.leer)+posiblesVar):
                return True
            else:
                return False #se mostraria un error en la pantalla 

    def agregarKernelMemoria(self):   
        i=0
        memVacia = ""
        try:
            memVacia = self.memoria[1]
        except:
            memVacia =""

        if(self.proEjec == 0) and memVacia == "":
            for i in range(self.kernel):
                self.memoria.append("***kernel ch***")
        else:
            print('no hay necesidad de agregar kernel')
    

    #metodo para agregar las instrucciones a la memoria 
    def agregarInstrMemoria(self): # idProg la variable global es proEjec, este metodo puede ser llamado desde views
        for i in range(len(self.leer)):
            if i==0:
                self.rb.append(len(self.memoria))# para saber donde inicia el programa ---------- #self.rb[self.proEjec]=len(self.memoria)  
                self.memoria.append(self.leer[i].rstrip()) 
            elif i == len(self.leer)-1:
                self.rlc.append(len(self.memoria)+1)# para saber donde termina el programa --------- #self.rlc[self.proEjec] = len(self.memoria) 
                self.memoria.append(self.leer[i].rstrip()) 
            else:
                self.memoria.append(self.leer[i].rstrip())
        ################################ se agregan estas instrucciones para tener el rlp
        posiblesVar = 0
        for i in range(len(self.leer)):
            palabras = self.leer[i].rstrip().split()
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        for i in range(len(self.rlc)): # se delimita el registro limite del programa 
            self.rlp.append(self.rlc[self.proEjec] + posiblesVar)
        ##############################
        self.cantmemoria -= ((self.rlc[self.proEjec]- self.rb[self.proEjec]) + posiblesVar) # se resta el espacio que ocupa el programa con su variables 
    
    def agregarEtiquetas(self): # se hace necesario agregar las etiquetas puesto que se pueden usar antes de ser cargadas 
        instruc=[] # numero de la instruccion hacia donde debe ir 
        #for i in range(len(self.leer)):
        for i in range(self.rb[self.proEjec],self.rlc[self.proEjec]):
            palabras = self.memoria[i].split()
            operador = palabras[0]
            if operador == 'etiqueta':
                self.etiquetas.append(str(self.proEjec) + '-' + str(palabras[1])) # guardamos el nombre de la etiqueta
                instruc.append(int(palabras[2])) #se agrega a que numero de linea se debe ir con respecto a la etiqueta
                
       

        p=0#maneja el indice de la lista instruc donde se tiene a que numero de instruccion  se debe ir ejem: etiqueta algo 8, debe ir a la linea 8 del archivo .ch
        bandera=True # variable bandera para manterner la ejecucion del ciclo for hasta que se tengan todas las posiciones de memoria realacionadas con la linea que buscamos
        while(bandera): 
            k=1 # contador de lineas en el archivo  
            for i in range(self.rb[self.proEjec],self.rlc[self.proEjec]): # posiciones de memoria del archivo
                if p < len(instruc): # verifica que no se exceda el arreglo que tiene a que numero de instruccion se debe ir 
                    if instruc[p] == k: 
                        self.posMemEtiq.append(i) # se agrega la posicion de memoria correspondiente con el numero de la instruccion que se buscaba 
                        p+=1 # se cambia a el siguiente indice de la lista instruc
                        k+=1 # se suma 1 para evitar los conflictos a la hora de ejecutar el ciclo for
                    else:
                        k+=1 # se suma 1 continuar con la busqueda del numero indicado de instruccion deseada 
                else:
                    bandera=False

    #metodo que realiza la ejecución del programa
    def ejecutarProg(self, posMemEjec): # posMemEjec se requerirá si se llega  a una instrucción vaya o vayasi para cambiar la ejecucion del programa
        # proEjec no se envia como parametro, porque no se conoce cuando se realice el primer llamado en views
        numlea =0
        varEjer = 0 # esta variable cambiara dependiendo si es una ejecucion normal o si se ingresa el parametro posMemEjec para cambiar la ejecucion a una linea especifica
        
        if int(posMemEjec) >=0: #si se llega a cambiar el orden de ejecucion del programa
            varEjer = posMemEjec 
        else:
            varEjer = self.rb[self.proEjec]
            self.agregarEtiquetas() # se agregan las etiquetas del programa

        for i in range(varEjer,self.rlc[self.proEjec]):
            palabras = self.memoria[i].rstrip().split()
            operador = palabras[0]
        
            if operador == 'cargue':
                self.eCargue(palabras, self.proEjec) 
            elif operador == 'almacene':
                self.eAlmacene(palabras, self.proEjec)
            elif operador == 'vaya':
                self.eVaya(palabras, self.proEjec)
            elif operador == 'nueva':
                self.eNueva(palabras, self.proEjec)
            elif operador == 'etiqueta':
                pass
            elif operador == 'lea':
                self.eLea(palabras,self.proEjec, numlea) 
                numlea +=1
            elif operador == 'sume':
                self.eSume(palabras, self.proEjec)
            elif operador == 'reste':
                self.eReste(palabras, self.proEjec)
            elif operador == 'multiplique':
                self.eMultiplique(palabras, self.proEjec)
            elif operador == 'divida':
                self.eDivida(palabras, self.proEjec)
            elif operador == 'potencia':
                self.ePotencia(palabras, self.proEjec)
            elif operador == 'modulo':
                self.eModulo(palabras, self.proEjec)
            elif operador == 'concatene':
                self.eConcatene(palabras, self.proEjec)
            elif operador == 'elimine':
                self.eElimine(palabras, self.proEjec)
            elif operador == 'extraiga':
                self.eExtraiga(palabras, self.proEjec)
            elif operador == 'Y':
                self.eY(palabras, self.proEjec)
            elif operador == 'O':
                self.eO(palabras, self.proEjec)
            elif operador == 'NO':
                self.eNo(palabras, self.proEjec)
            elif operador == 'muestre' and varEjer == self.rb[self.proEjec]: #se verifica que sea la ejecucion base para evitar que se repitan valores
                self.eMuestre(palabras, self.proEjec)
            elif operador == 'imprima' and varEjer == self.rb[self.proEjec]: #se verifica que sea la ejecucion base para evitar que se repitan valores
                self.eImprima(palabras, self.proEjec)
            elif operador == 'absoluto':
                self.eAbsoluto(palabras, self.proEjec)
            elif operador == 'vayasi':
                self.eVayaSi(palabras, self.proEjec)   

            elif operador == 'retorne' and varEjer == self.rb[self.proEjec]: #se verifica que sea la ejecucion base para evitar que se repitan valores
                self.pantalla.append("*****************************")
                self.pantalla.append("se finalizó la ejecución del programa: " + str(self.proEjec))
                self.pantalla.append("*****************************")
            else:
                pass
       
    #############################################################################################################################
    #metodos para obterner los valores y mostrarlos en el frontend

    #metodo para obtener lo que será mostrado en pantalla
    def getPantalla(self):
        return self.pantalla

    #metodo para obtener lo que será mostrado en la impresora
    def getImpresora(self):
        return self.impresora

    #metodo para obtener el valor del acumulador (acumulador en el frontend)
    def getAcumulador(self):
        for i in range(len(self.memoria)): #se hace el ciclo for para que se vaya actualizando el valor a medida que se ejecuta el prog
            tempoVar = self.memoria[0]
        return str(tempoVar)
    
    #metodo para obtener la linea que se esta ejecutando (pc en el frontend)
    def getLineaActual(self):
        tempoVar="" 
        try:
            i= self.rb[self.proEjec]
            for i in range(self.rlc[self.proEjec]):
                tempoVar = self.memoria[i]

        except:
            tempoVar=""
        
        return str(tempoVar)

    #metodo para mostrar el codigo y las posiciones de memoria que ocupa
    def getCodProgActual(self): # metodo definitivo pendiente actualizar los demas
        tempoDic ={} # se usa un diccionario para facilitar la compatibilidad con el frontend
        try: 
            for j in range(self.rb[self.proEjec], self.rlc[self.proEjec]): # se toma el codigo del programa en ejecucion desde donde empieza en la memoria hasta donde termina 
                tempoDic[j] =self.memoria[j]
        except:
            tempoDic ={}
        return tempoDic 

   
    #metodo para obtener cada variable que esta memoria del programa que se esta ejecutando (variables en el frontend)
    def getVariablesActuales(self):
        i= 0
        tempoDic={} # se usa un diccionario para facilitar la manera de mostrar los datos en el frontend
        for i in range(len(self.variables)):
            palabras = self.variables[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== str(self.proEjec): 
                tempoDic[self.posMemVar[i]]= self.variables[i]
        return tempoDic
    
    #metodo para obtener cada etiqueta que esta memoria del programa que se esta ejecutando (etiquetas en el frontend)
    def getEtiquetasActuales(self):
        i= 0
        tempoDic={} # se usa un diccionario para facilitar la manera de mostrar los datos en el frontend
        for i in range(len(self.etiquetas)):
            palabras = self.etiquetas[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== str(self.proEjec): 
                tempoDic[self.posMemEtiq[i]]= self.etiquetas[i]
        return tempoDic
    
    #metodo para retornar lo que se encuentra en la memoria 
    def getMemoria(self):
        tempoDic ={} # se usa un diccionario para facilitar la compatibilidad con el frontend
        for j in range(len(self.memoria)): # se toma el codigo del programa en ejecucion desde donde empieza en la memoria hasta donde termina 
            tempoDic[j] =self.memoria[j]
        return tempoDic 
    
    #metodo para obtener cada etiqueta que esta memoria del programa que se esta ejecutando (etiquetas en el frontend)
    def getProgramas(self):
        i= 0
        tempoDic={} # se usa un diccionario para facilitar la manera de mostrar los datos en el frontend
        try:
            for i in range(len(self.ruta2)):
                palabras = str(self.ruta2[i]).split('/') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
                tempoDic[i]= {'prog':palabras[1], 'ins': int(self.rlc[i] - self.rb[i]),'rb':self.rb[i], 'rlc':self.rlc[i]-1, 'rlp':self.rlp[i]-1}
        except:
            tempoDic={}
        return tempoDic
    
    def getMemoriaDispo(self):
        libre = []
        for i in range(self.cantidadFull - len(self.memoria)):
            libre.append(len(self.memoria) + i) # (se resta el acumulador) ---------> se restan dos, porque se quita el acumulador y el tamaño siempre es 1 mas grande
        return libre
    
    ###########################################################################################################################################################

    #metodos auxiliares para identificar variables o etiquetas dentro de la memororia 

    # identificar la etiqueta en memoria
    def idenEtiq(self, nomEtiq, idProg):
        posMem = 0
        indice = 0
        for i in range(len(self.etiquetas)):
            palabras = self.etiquetas[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la etiqueta
            if palabras[0]== str(idProg) and palabras[1] == nomEtiq:
                indice=i
        posMem = self.posMemEtiq[indice]
        return posMem   


    #metodo para agregar la variable a una lista con su id corresponidiente

    def varConIdProg(self, idProg, nombVar, posMemoria): # idProg > id  del programa y nombre de la variable 
        self.posMemVar.append(posMemoria) # posMemVar es global
        self.variables.append(str(idProg) + "-"+ nombVar)
        

    #metodo para identificar una linea especifica dentro de la memoria, se usará para las etiquetas 

    def encontrarLinea(self, i):
       # return self.leer[i-1].rstrip()
        return self.leer[int(i)-1].rstrip()
    

    #identificar la variable en memoria

    def idenVar(self, nomVar, idProg):
        posMem = 0
        indice = 0
        for i in range(len(self.variables)):
            palabras = self.variables[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0] == str(idProg) and str(palabras[1]) == nomVar:
                indice=i
        posMem = self.posMemVar[indice]
        return posMem
    ############################################################################################################################################
  
    # metodos para ejecutar cada operando del arhivo .ch 
    
    def eNueva(self, linea, idProg):
        if(len(linea)==4) :
            if linea[2] == 'I':
                #con este segmento convierto a int la variable y el acumulador si es posible 
                #####################################
                anumeroIntVar = 0
                varInt = False # corresponde al valor que se encuentra en la variable
                try:
                    anumeroIntVar = int(linea[3])
                    varInt = True
                except:
                    varInt = False
                    print('no se pudo convertir a entero la variable en nuevaVar')
                ############################################# 
                if varInt:
                    self.memoria.append(int(linea[3]))
                    self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                    self.cantidVarixPro[idProg] += 1
                else:
                    print('no se convirtio a entero') 
                
            elif linea[2] == 'R':
                #con este segmento convierto a real la variable y el acumulador si es posible 
                #############################################
                anumeroFloatVar = 0.0
                varFloat = False # corresponde al valor que se encuentra en la variable
                try:
                    anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
                    varFloat = True
                except:
                    varFloat = False
                    self.pantalla.append('no se pudo convertir a real la variable')
                ############################################# 
                if varFloat:
                    self.memoria.append(float(linea[3]))
                    self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                    self.cantidVarixPro[idProg] += 1
                else:
                    print('no se convirtio a real')
                
            elif linea[2] == 'L':
                #con este segmento convierto a int la variable y el acumulador si es posible 
                #####################################
                anumeroIntVar = 0
                varIntL = False # corresponde al valor que se encuentra en la variable
                try:
                    anumeroIntVar = int(linea[3])
                    varIntL = True
                except:
                    varIntL = False
                    print('no se pudo convertir a entero la variable')
                ############################################# 
                if varIntL:
                    self.memoria.append(int(linea[3]))
                    self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                    self.cantidVarixPro[idProg] += 1
                else:
                    print('no se convirtio a lógico') 

            elif linea[2] == 'C':
                self.memoria.append(linea[3])
                self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                self.cantidVarixPro[idProg] += 1
            
            else:
                print('no se agrego nada nuevo')
            
        elif (len(linea)==3):
            if linea[2] == 'I':
                self.memoria.append(0)
                self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                self.cantidVarixPro[idProg] += 1

            elif linea[2] == 'R':
                self.memoria.append(0.0)
                self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                self.cantidVarixPro[idProg] += 1

            elif linea[2] == 'L':
                self.memoria.append(0)
                self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                self.cantidVarixPro[idProg] += 1

            else:
                self.memoria.append('')
                self.varConIdProg(idProg, linea[1], len(self.memoria)-1)
                self.cantidVarixPro[idProg] += 1
        else:
            self.pantalla.append('no se agregó nada nuevo')
        
    #fin funcion sNueva

    def eCargue(self, linea, idProg):
        self.memoria[0] = self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
       
    def eAlmacene(self, linea, idProg):
        self.memoria[self.idenVar(linea[1],idProg)] = self.memoria[0] # se identifica la posicion de memoria y se trae el valor del acumulador

    def eSume(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if varInt and acumInt: #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper += int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat:
            oper=float(self.memoria[0])
            oper += float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat:
            oper=float(self.memoria[0])
            oper += int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt:
            oper=int(self.memoria[0])
            oper += float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        else:
            self.pantalla.append("error al sumar no corresponden los tipos")

    def eReste(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if varInt and acumInt: #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper -= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat:
            oper=float(self.memoria[0])
            oper -= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat:
            oper=float(self.memoria[0])
            oper -= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt:
            oper=int(self.memoria[0])
            oper -= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        else:
            self.pantalla.append("error al restar, no corresponden los tipos")
    
    def eMultiplique(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if varInt and acumInt: #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper *= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat:
            oper=float(self.memoria[0])
            oper *= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat:
            oper=float(self.memoria[0])
            oper *= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt:
            oper=int(self.memoria[0])
            oper *= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        else:
            self.pantalla.append("error al multiplicar, no corresponden los tipos")
    

    def eDivida(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  
        if varInt and acumInt and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0): #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper /= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=float(self.memoria[0])
            oper /= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=float(self.memoria[0])
            oper /= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=int(self.memoria[0])
            oper /= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        
        elif (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar == 0 or anumeroFloatVar == 0.0):
            self.pantalla.append("error al dividir, division por Cero")
        else:
            self.pantalla.append("error al dividir, no corresponden los tipos")
    
    def ePotencia(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if varInt and acumInt: #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper **= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat:
            oper=float(self.memoria[0])
            oper **= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat:
            oper=float(self.memoria[0])
            oper **= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt:
            oper=int(self.memoria[0])
            oper **= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        else:
            self.pantalla.append("error al elevar la potencia, no corresponden los tipos")
    
    def eModulo(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntVar = 0
        anumeroIntAcum = 0
        varInt = False # corresponde al valor que se encuentra en la variable
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntVar = int(self.memoria[self.idenVar(linea[1],idProg)])
            varInt = True
        except:
            varInt = False
            self.pantalla.append('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatVar = 0.0
        anumeroFloatAcum = 0.0
        varFloat = False # corresponde al valor que se encuentra en la variable
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatVar = float(self.memoria[self.idenVar(linea[1],idProg)])
            varFloat = True
        except:
            varFloat = False
            self.pantalla.append('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if varInt and acumInt and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0): #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper %= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif varFloat and acumFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=float(self.memoria[0])
            oper %= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=float(self.memoria[0])
            oper %= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varFloat and acumInt and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            oper=int(self.memoria[0])
            oper %= float(self.memoria[self.idenVar(linea[1],idProg)]) 
            self.memoria[0] = oper
        
        elif (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar == 0 or anumeroFloatVar == 0.0):
            self.pantalla.append("error al tomar el modulo, division por Cero")
        else:
            self.pantalla.append("error al tomar el modulo, no corresponden los tipos")
    
    def eAbsoluto(self, linea, idProg):
        #con este segmento convierto a int la variable y el acumulador si es posible 
        #####################################
        anumeroIntAcum = 0
        acumInt = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla.append('no se pudo convertir a entero el acumulador')
        #############################################  
        #con este segmento convierto a real la variable y el acumulador si es posible 
        #############################################
        anumeroFloatAcum = 0.0
        acumFloat = False # corresponde al valor que se encuentra en el acumulador
        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla.append('no se pudo convertir a real el acumulador')
        #############################################  

        if (acumInt):
            oper= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[self.idenVar(linea[1],idProg)] = abs(int(self.memoria[0]))
            self.memoria[self.idenVar(linea[1],idProg)] = oper
        elif acumFloat:
            oper= float(self.memoria[self.idenVar(linea[1],idProg)])
            oper= abs(float(self.memoria[0])) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[self.idenVar(linea[1],idProg)] = oper 
        else:
            self.pantalla.append("error no se puede tomar el valor absoluto, no corresponden los tipos")

    def eConcatene(self, linea, idProg):
        cadAcum = str(self.memoria[0])
        cadVar = str(self.memoria[self.idenVar(linea[1],idProg)])
        self.memoria[0] =cadAcum + cadVar

    def eElimine(self, linea, idProg):
        varTem = self.memoria[0].replace(self.memoria[self.idenVar(linea[1],idProg)],"") # se guara en una variable temporal el resultado de quitar la cadena en Variable a el acumulador
        self.memoria[0] = varTem

    def eExtraiga(self, linea, idProg):
        varTem = str(self.memoria[0])
        self.memoria[0] = varTem[:self.memoria[self.idenVar(linea[1],idProg)]] # se extraen los primeros(cantidad que esté en la variable) caracteres de la cadena que se encuentra en el acumulador 
    
    def eY(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if int(var1) ==0:
            var1Bol=False
        elif int(var1) ==1:
            var1Bol = True 
        else:
            self.pantalla.append("la variable 1 no es de tipo lógico")
        
        if int(var2) ==0:
            var2Bol=False
        elif int(var2) ==1:
            var2Bol = True 
        else:
            self.pantalla.append("la variable 2 no es de tipo lógico")

        self.memoria[self.idenVar(linea[3],idProg)] = var1Bol and var2Bol

    def eO(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if int(var1) ==0:
            var1Bol=False
        elif int(var1) ==1:
            var1Bol = True 
        else:
            self.pantalla.append("la variable 1 no es de tipo lógico" )
        
        if int(var2) ==0:
            var2Bol=False
        elif int(var2) ==1:
            var2Bol = True 
        else:
            self.pantalla.append("la variable 2 no es de tipo lógico")

        self.memoria[self.idenVar(linea[3],idProg)] = var1Bol or var2Bol

    def eNo(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if int(var1) ==0:
            var1Bol=False
        elif int(var1) ==1:
            var1Bol = True 
        else:
            self.pantalla.append("la variable 1 no es de tipo lógico")  

        self.memoria[self.idenVar(linea[2],idProg)] = not(var1Bol)
    
    def eMuestre(self, linea, idProg):
        if(linea[1]=='acumulador'):
            self.pantalla.append(str(self.memoria[0]))
        else:
           self.pantalla.append(str(self.memoria[self.idenVar(linea[1],idProg)]))

    def eImprima(self, linea, idProg):
        if(linea[1]=='acumulador'):
            self.impresora.append(str(self.memoria[0]))
        else:
            self.impresora.append(str(self.memoria[self.idenVar(linea[1],idProg)]))    

    def eEtiqueta(self, linea, idProg):
        
        self.etiquetas.append(str(idProg) + '-' +str(linea[1]) ) # guardamos el nombre de la etiqueta
        instruccion = self.encontrarLinea(linea[2]) # identificamos a que instruccion se refiere la etiqu
        posMemoriaEti = 0 # variable temporal

        i=self.rb[idProg] # con esto identificamos donde inicia el programa 
        for i in range(self.rlc[idProg]): # ciclo que recorre solamente las posiciones de memoria que corresponden a las instrucciones
            if instruccion == self.memoria[i]:
                posMemoriaEti = i
                break
        self.posMemEtiq.append(posMemoriaEti) # se agrega la posicion de memoria de la instruccion a donde apunta la etiq

    def eVaya(self, linea, idProg):
        posMemEti = self.idenEtiq(linea[1], idProg)
        self.ejecutarProg(posMemEti)#aquí se llama el metodo donde cambiará el flujo del programa con la posicion de memoria de la etiqueta
    
    def eVayaSi(self, linea, idProg):
        posMemEti1 = self.idenEtiq(linea[1], idProg)
        posMemEti2 = self.idenEtiq(linea[2], idProg)

        if int(self.memoria[0]) > 0 or float(self.memoria[0])> 0.0:
            self.ejecutarProg(posMemEti1) # #aquí se llama el metodo donde cambia el flujo del programa con la posicion que entregue (posMemEti1)
            
        elif int(self.memoria[0]) < 0 or float(self.memoria[0])< 0.0:
            self.ejecutarProg(posMemEti2) # #aquí se llama el metodo donde cambia el flujo del programa con la posicion que entregue (posMemEti2)
            
        else:
            print('continuando con la ejecucion')
            pass

    def eLea(self, linea, idProg, enQueLeerVa):
        valorLeido = ""
        global valoresLeidos

        try:
            valorLeido = valoresLeidos[enQueLeerVa]
        except :
            valorLeido = -1

        self.memoria[self.idenVar(linea[1],idProg)] = valorLeido #guarda la posicion de memoria 
    
    def clean(self):
        self.cantmemoria= 0 
        self.cantidadFull = 0 #cantidad full de memoria
        self.kernel= 0
        self.proEjec=0 # id del programa que se ejecuta actualmente
        self.leer=[] # todas las lineas del codigo del programa .ch
        self.ruta2=[]
        self.memoria =[] # memoria donde se guarda el kernel, los programas y el acumulador
        self.variables =[] #aqui se guardan los nombres de las variables
        self.posMemVar=[]
        self.cantidVarixPro=[0]*30 # aqui se sabe cuantas variables son agregadas en cada uno de los programas, que representan una posicion en el arreglo 
        self.etiquetas =[] #aqui se guardan los nombres de la etiquetas
        self.posMemEtiq=[]
        self.rb=[] # registro base del programa, donde empieza el programa, cada posicion corresponde a un programa (ejem rb[0] es el rb del programa 0)
        self.rlc =[] # registro limite del codigo, hasta donde llegan las instrucciones del programa, cada posicion corresponde a un programa (ejem rlc[0] es el rlc del programa 0) 
        self.rlp=[] # registro limite del programa, hasta donde llega el programa, con variables incluidas, cada posicion corresponde a un programa (ejem rlp[0] es el rlp del programa 0)
        self.pantalla =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
        self.impresora =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
        valoresLeidos=[] #valor traido desde el front para la funcion leer

