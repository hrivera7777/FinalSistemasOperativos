from django.core.files import File
from .models import EjecArchCh
"""
ruta =""
#tup = ArchivosCh.objects.all()
tup2 = EjecArchCh.objects.all()
#aqui se agregan todos los archivos para abrir 
ruta2=[]
w=0
cantmemoria=-2
kernel=-3


for tp in tup2:
    nombre2=tp.archivo
    tempo = tp.memoria
    cantmemoria=int(tempo) # cantidad total de memoria, se va disminuyendo si se agrega el kernel o programas
    tempo = tp.kernel
    kernel=int(tempo)
    ruta2.append(str(nombre2))

proEjec=len(tup2)-1 #cual programa se encuentra en ejecución  

print(ruta2)
"""

"""
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
"""

class ejecucion:
    ruta =""
    #tup = ArchivosCh.objects.all()
    tup2 = EjecArchCh.objects.all()
    #aqui se agregan todos los archivos para abrir 
    ruta2=[] #ok
    w=0
    cantmemoria=-2
    kernel=-3

    tp =[]
    tempo=""
    nombre2=""
    proEjec=0
    for tp in tup2:
        nombre2=tp.archivo
        tempo = tp.memoria
        cantmemoria=int(tempo) # cantidad total de memoria, se va disminuyendo si se agrega el kernel o programas
        tempo = tp.kernel
        kernel=int(tempo)
        ruta2.append(str(nombre2))
        tempo = tp.id
        #print(tempo)
        #proEjec= int(tempo)

    #proEjec=len(tup2)-1 #cual programa se encuentra en ejecución  

    #print(ruta2)

    f = open("media/" + ruta2[proEjec], "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.readlines() #para leer linea a linea #print(leer)
    f.close()
    myfile.close()
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
    pantalla ="" # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    impresora ="" # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    
    ###############################################################################
    # necesasario para quitar el \n que se genera en algunos archivos .ch
    contadorSalto=0 # contador de salto de linea
    i=0
    contraS=""
    w=0
    for w in range(len(leer)):  
        contraS = leer[w] # variable para verificar si hay un salto de linea
        if contraS == str('\n'):
            contadorSalto +=1
    j=0
    for j in range(contadorSalto):
        leer.remove(str('\n'))
    ################################################################################

    

    # metodo que comprueba si es posible realizar la ejecución (la memoria debe ser mayor al kernel)
    def puedeEjecKernel(self):
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
            #print(palabras)
            operador = palabras[0]
            if operador == 'nueva':
                posiblesVar +=1
        if self.cantmemoria >= (len(self.leer)+posiblesVar): 
            self.cantmemoria -= len(self.leer)
            return True
        else:
            return False #se mostraria un error en la pantalla 
    

    #aquí se llena la memoria con el "kernel"
    def agregarKernelMemoria(self):   
        i=0
        for i in range(self.kernel):
            self.memoria.append("***kernel ch***")
    

    #metodo para agregar las instrucciones a la memoria 
    def agregarInstrMemoria(self): # idProg la variable global es proEjec, este metodo puede ser llamado desde views
        for i in range(len(self.leer)):
            if i==0:
                self.rb.append(len(self.memoria)) #self.rb[self.proEjec]=len(self.memoria) # para saber donde inicia el programa 
                self.memoria.append(self.leer[i].rstrip()) 
            elif i == len(self.leer)-1:
                self.rlc.append(len(self.memoria)+1) #self.rlc[self.proEjec] = len(self.memoria) # para saber donde termina el programa
                self.memoria.append(self.leer[i].rstrip()) 
            else:
                self.memoria.append(self.leer[i].rstrip()) 
            
    #metodo que realiza la ejecución del programa
    def ejecutarProg(self, posMemEjec): # posMemEjec se requerirá si se llega  a una instrucción vaya o vayasi para cambiar la ejecucion del programa
        # proEjec no se envia como parametro, porque no se conoce cuando se realice el primer llamado en views
        
        varEjer = 0 # esta variable cambiara dependiendo si es una ejecucion normal o si se ingresa el parametro posMemEjec para cambiar la ejecucion a una linea especifica
        
        if posMemEjec >=0: #si se llega a cambiar el orden de ejecucion del programa
            varEjer = posMemEjec 
        else:
            varEjer = self.rb[self.proEjec] 
        #print(self.rlc)
        for i in range(varEjer,self.rlc[self.proEjec]):
            palabras = self.memoria[i+1].rstrip().split()
            #print(palabras)
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
                self.eEtiqueta(palabras, self.proEjec)
            elif operador == 'lea':
                pass#self.eLea(palabras, self.proEjec)
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
            elif operador == 'muestre':
                self.eMuestre(palabras, self.proEjec)
            elif operador == 'imprima':
                self.eImprima(palabras, self.proEjec)
            elif operador == 'absoluto':
                self.eAbsoluto(palabras, self.proEjec)
            elif operador == 'vayasi':
                self.eVayaSi(palabras, self.proEjec)
            elif operador == 'retorne':
                self.pantalla += "\n se finalizó la ejecución del programa "
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
        i= self.rb[self.proEjec]
        for i in range(self.rlc[self.proEjec]):
            tempoVar = self.memoria[i]
        return str(tempoVar)

    #metodo prueba
    def getCodProgActualMod(self): # metodo definitivo pendiente actualizar los demas

        i= self.rb[self.proEjec]
        print(i)
        tempoDic ={}
        for j in range(i, self.rlc[self.proEjec]):
            tempoDic[j] =self.memoria[j]
        print(type(tempoDic))
        return tempoDic 

    """
    def getCodProgActualMod(self):

        i= self.rb[self.proEjec]
        print(i)
        tempoList =[[],[]]
        for j in range(i, self.rlc[self.proEjec]):
            tempoList[0].append(j) 
            tempoList[1].append(self.memoria[j])
        print(type(tempoList))
        return tempoList 
    """
    #metodo para obtener cada linea que se esta ejecutando (instruccion en el frontend)
    def getPosCodProgActual(self):
        i= self.rb[self.proEjec]
        print(i)
        tempoList =[]
        for j in range(i, self.rlc[self.proEjec]):
            print(i,'dentro')
            tempoList.append(j) 
        return tempoList 

    #metodo para obtener cada linea que se esta ejecutando (instruccion en el frontend)
    def getCodProgActual(self):
        return self.leer 

    """
    def getCodProgActual(self):
        i= self.rb[self.proEjec] 
        tempoList=[]
        for k in range(i, self.rlc[self.proEjec]):
            tempoList.append(self.memoria[k])
        return tempoList
    """
    #metodo para obtener cada posicion de memoria de cada linea que se esta ejecutando (memoria (al lado izq instruccion) en el frontend)
    def getProgActual(self):
        i= self.rb[self.proEjec]
        tempoList=[]
        for i in range(self.rlc[self.proEjec]):
             tempoList[i] = i
        return  tempoList
    
    #metodo para obtener cada variable que esta memoria del programa que se esta ejecutando (variables en el frontend)
    def getVariablesActuales(self):
        i= 0
        tempoList=[]
        j=0
        for i in range(len(self.variables)-1):
            palabras = self.variables[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== self.proEjec: 
                tempoList[j]= self.variables[i]
                j +=1
        return tempoList
    
    #metodo para obtener cada posicion de memoria de la variable que esta memoria del programa que se esta ejecutando (pos al la izq de variables en el frontend)
    def getPosVariablesActuales(self):
        i= 0
        tempoList=[]
        j=0
        for i in range(len(self.variables)-1):
            palabras = self.variables[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== self.proEjec:
                tempoList[j]= self.posMemVar[i]
                j +=1
        return tempoList

    #metodo para obtener cada etiqueta que esta memoria del programa que se esta ejecutando (etiquetas en el frontend)
    def getEtiquetasActuales(self):
        i= 0
        tempoList=[]
        j=0
        for i in range(len(self.etiquetas)-1):
            palabras = self.etiquetas[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== self.proEjec:
                tempoList[j]= self.etiquetas[i]
                j +=1
        return tempoList

    #metodo para obtener cada posicion de memoria de la variable que esta memoria del programa que se esta ejecutando (pos al la izq de variables en el frontend)
    def getPosEtiquetasActuales(self):
        i= 0
        tempoList=[]
        j=0
        for i in range(len(self.etiquetas)-1):
            palabras = self.etiquetas[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== self.proEjec:
                tempoList[j]= self.posMemEtiq[i]
                j +=1
        return tempoList
    
    #metodo para retornar lo que se encuentra en la memoria 
    def getMemoria(self):
        return self.memoria

    #metodo para retornar lo las posiciones en la memoria 
    def getPosMemoria(self):
        tempoList = []
        for i in range(len(self.memoria)-1):
            tempoList.append(i) 
        return tempoList 

    #metodo para retornar los registros bases de los programas 
    def getRegistroBase(self):
        return self.rb   

    #metodo para retornar los registros limites del codigo relacionado con los programas 
    def getRegistroLimCod(self):
        return self.rlc

    #metodo para retornar los registros limites del programa que incluye las variables relacionado con los programas
    def getRegistroLimProg(self):
        for i in range(len(self.rlc)):
            self.rlp.append(self.rlc[self.proEjec] + self.cantidVarixPro[self.proEjec])
        return self.rlp

    def getProgramas(self):
        progList =[]
        for i in range(len(self.ruta2)):
            tempo2= str(self.ruta2[i]).split('/')
            progList.append(tempo2[1])
        return progList
    
    def getIdProg(self):
        return self.proEjec
    
    def getCanInstProg(self):
        #return len(self.leer)
        return int(self.rlc[self.proEjec] - self.rb[self.proEjec])

    def getMemoriaDispo(self):
        libre = []
        for i in range(self.cantmemoria-1):
            libre.append(len(self.memoria) - 2 + i) # se restan dos, porque se quita el acumulador y el tamaño siempre es 1 mas grande
        return libre
        
    ###########################################################################################################################################################

    #metodos auxiliares para identificar variables o etiquetas dentro de la memororia 

    # identificar la etiqueta en memoria
    def idenEtiq(self, nomEtiq, idProg):
        posMem = 0
        indice = 0
        for i in range(len(self.etiquetas)-1):
            palabras = self.etiquetas[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la etiqueta
            if palabras[0]== idProg and palabras[1] == nomEtiq:
                indice=i

        posMem = self.posMemVar[indice]
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
        for i in range(len(self.variables)-1):
            palabras = self.variables[i].split('-') # con palabras se crea un array y ahí la posicion 0 es el id del programa y la posicion 1 es el nombre de la variable
            if palabras[0]== idProg and palabras[1] == nomVar:
                indice=i

        posMem = self.posMemVar[indice]
        return posMem
    ############################################################################################################################################
  
    # metodos para ejecutar cada operando del arhivo .ch 
    
    def eNueva(self, linea, idProg):
        if(len(linea)==4) :
            self.memoria.append(linea[3])
            self.varConIdProg(idProg, linea[1],len(self.memoria))
            self.cantidVarixPro[idProg] += 1
            
        elif (len(linea)==3):
            if linea[2] == 'I':
                self.memoria.append(0)
                self.varConIdProg(idProg, linea[1], len(self.memoria))
                self.cantidVarixPro[idProg] += 1

            elif linea[2] == 'R':
                self.memoria.append(0.0)
                self.varConIdProg(idProg, linea[1], len(self.memoria))
                self.cantidVarixPro[idProg] += 1

            elif linea[2] == 'L':
                self.memoria.append(0)
                self.varConIdProg(idProg, linea[1], len(self.memoria))
                self.cantidVarixPro[idProg] += 1

            else:
                self.memoria.append('')
                self.varConIdProg(idProg, linea[1], len(self.memoria))
                self.cantidVarixPro[idProg] += 1
        else:
            self.pantalla = 'no se agregó nada nuevo'
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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real la variable'

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  

        if varInt and varFloat: #(varInt or varFloat) and (acumInt or acumFloat):
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
            self.pantalla = "error al sumar no corresponden los tipos"

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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real la variable'

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  

        if varInt and varFloat: #(varInt or varFloat) and (acumInt or acumFloat):
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
            self.pantalla = "error al restar, no corresponden los tipos"
    
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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real la variable'

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  

        if varInt and varFloat: #(varInt or varFloat) and (acumInt or acumFloat):
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
            self.pantalla = "error al multiplicar, no corresponden los tipos"
    

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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real la variable'

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  
        if varInt and varFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0): #(varInt or varFloat) and (acumInt or acumFloat):
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
            self.pantalla = "error al dividir, division por Cero"
        else:
            self.pantalla = "error al dividir, no corresponden los tipos"
    
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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  

        if varInt: #(varInt or varFloat) and (acumInt or acumFloat):
            oper=int(self.memoria[0])
            oper **= int(self.memoria[self.idenVar(linea[1],idProg)]) # se identifica la posicion de memoria y se trae el valor al acumulador
            self.memoria[0] = oper

        elif acumFloat:
            oper=float(self.memoria[0])
            oper **= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif varInt and acumFloat:
            oper=float(self.memoria[0])
            oper **= int(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper

        elif acumInt:
            oper=int(self.memoria[0])
            oper **= float(self.memoria[self.idenVar(linea[1],idProg)])
            self.memoria[0] = oper
        else:
            self.pantalla = "error al elevar la potencia, no corresponden los tipos"
    
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
            self.pantalla = 'no se pudo convertir a entero la variable'
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real la variable'

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            self.pantalla = 'no se pudo convertir a real el acumulador'
        #############################################  

        if varInt and varFloat and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0): #(varInt or varFloat) and (acumInt or acumFloat):
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
            self.pantalla = "error al tomar el modulo, division por Cero"
        else:
            self.pantalla = "error al tomar el modulo, no corresponden los tipos"
    
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
            self.pantalla = 'no se pudo convertir a entero el acumulador'
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
            self.pantalla = 'no se pudo convertir a real el acumulador'
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
            self.pantalla = "error no se puede tomar el valor absoluto, no corresponden los tipos"

    def eConcatene(self, linea, idProg):
        cadAcum = str(self.memoria[0])
        cadVar = str(self.memoria[self.idenVar(linea[1],idProg)])
        self.memoria[0] =cadAcum + cadVar

    def eElimine(self, linea, idProg):
        varTem = self.memoria[0].replace(self.memoria[self.idenVar(linea[1],idProg)],"") # se guara en una variable temporal el resultado de quitar la cadena en Variable a el acumulador
        self.memoria[0] = varTem
        """
        variable = "quedeque" # ejemplo de elimine
        var2 = variable.replace("que","")
        print(var2, len(var2))
        """
    def eExtraiga(self, linea, idProg):
        varTem = str(self.memoria[0])
        self.memoria[0] = varTem[:self.memoria[self.idenVar(linea[1],idProg)]] # se extraen los primeros(cantidad que esté en la variable) caracteres de la cadena que se encuentra en el acumulador 
    
    def eY(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if var1 ==0:
            var1Bol=False
        elif var1 ==1:
            var1Bol = True 
        else:
            self.pantalla = "la variable 1 no es de tipo lógico"
        
        if var2 ==0:
            var2Bol=False
        elif var2 ==1:
            var2Bol = True 
        else:
            self.pantalla = "la variable 2 no es de tipo lógico"

        self.memoria[self.idenVar(linea[3],idProg)] = var1Bol and var2Bol

    def eO(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if var1 ==0:
            var1Bol=False
        elif var1 ==1:
            var1Bol = True 
        else:
            self.pantalla = "la variable 1 no es de tipo lógico"  
        
        if var2 ==0:
            var2Bol=False
        elif var2 ==1:
            var2Bol = True 
        else:
            self.pantalla = "la variable 2 no es de tipo lógico" 

        self.memoria[self.idenVar(linea[3],idProg)] = var1Bol or var2Bol

    def eNo(self, linea, idProg):
        #valores boleanos son  0 para falso y 1 para verdadero

        var1 = linea[1] # aquí se toman los datos ingresados a la variable lógica 1
        var2= linea[2] # aquí se toman los datos ingresados a la variable lógica 2
        var1Bol = False # variable para convertir el dato(variable 1) ingresado a booleano 
        var2Bol = False # variable para convertir el dato(variable 2) ingresado a booleano 

        if var1 ==0:
            var1Bol=False
        elif var1 ==1:
            var1Bol = True 
        else:
            self.pantalla = "la variable 1 no es de tipo lógico"  

        self.memoria[self.idenVar(linea[2],idProg)] = not(var1Bol)
    
    def eMuestre(self, linea, idProg):
        if(linea[1]=='acumulador'):
            self.pantalla = str(self.memoria[0])
        else:
           self.pantalla = str(self.memoria[self.idenVar(linea[1],idProg)])

    def eImprima(self, linea, idProg):
        if(linea[1]=='acumulador'):
            self.impresora = str(self.memoria[0])
        else:
            self.impresora = str(self.memoria[self.idenVar(linea[1],idProg)])    

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

        if self.memoria[0] > 0:
            self.ejecutarProg(posMemEti1) # #aquí se llama el metodo donde cambia el flujo del programa con la posicion que entregue (posMemEti1)

        elif self.memoria[0] < 0:
            self.ejecutarProg(posMemEti2) # #aquí se llama el metodo donde cambia el flujo del programa con la posicion que entregue (posMemEti2)
        else:
            print('continuando con la ejecucion')
            pass


    """
    prueba local de la cantidad de memoria disponible 
    #print(memoria)
    #print(cantmemoria, 'cantidad de disponible')
    #print(len(memoria))
    #variables.append('0'+'-'+'variable')
    #print(variables)
    #palabras = variables[0].split('-')
    #print(palabras)
    """