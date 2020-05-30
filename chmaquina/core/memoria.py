
class memoria:
    memoria =[] # memoria donde se guarda el kernel, los programas y el acumulador
    kernel= 0
    cantmemoria= 0 
    cantidadFull = 0 #cantidad full de memoria (se necesita para calcular si se puede ejecutar el programa)

    memoria.append(0) # memoria en la primera posición será el acumudador (variable requerida en el ch máquina)
    cantmemoria -= 1 # aqui se disminuye en 1 cuando se toma el acumulador 

    rb=[] # registro base del programa, donde empieza el programa, cada posicion corresponde a un programa (ejem rb[0] es el rb del programa 0)
    rlc =[] # registro limite del codigo, hasta donde llegan las instrucciones del programa, cada posicion corresponde a un programa (ejem rlc[0] es el rlc del programa 0) 
    rlp=[] # registro limite del programa, hasta donde llega el programa, con variables incluidas, cada posicion corresponde a un programa (ejem rlp[0] es el rlp del programa 0)
    leer=[] # todas las lineas del codigo del programa .ch
    proEjec=0 # id del programa que se ejecuta actualmente

    def __init__(self,cantmemoria, cantKernel):
        self.cantmemoria = cantmemoria
        self.kernel=cantKernel
    

    def setProgEjec(self, progEjec): # introduce el programa en ejecucion 
        self.proEjec = progEjec
    
    def setLeer(self, leer): # introduce todas las lineas del archivo .ch
        self.leer = leer

    def setKernel(self, kernel): # introduce cantidad de memoria del programa en ejecucion
        self.kernel=kernel

    def setCantMemo(self, cantidMemo):  # introduce la cantidad de memoria del programa en ejecucion 
        if self.proEjec == 0:
            self.cantmemoria=cantidMemo
            self.cantidadFull = cantidMemo
        else:
            print('cantidad memoria else' + self.cantmemoria)
    
    #################################################################
    
    def getrb(self): # retorna el registro base del programa.
        return self.rb

    def getrlc(self): # retorna el registro límite de código 
        return self.rlc
    
    def getrlp(self):  # retorna el registro límite de programa 
        return self.rlp
    
    def getMemoria(self):
        return self.memoria

    def getMemoriaDispo(self):
        libre = []
        for i in range(self.cantidadFull - len(self.memoria)):
            libre.append(len(self.memoria) + i) # (se resta el acumulador) ---------> se restan dos, porque se quita el acumulador y el tamaño siempre es 1 mas grande
        return libre
    
    #metodo para retornar lo que se encuentra en la memoria 
    def getMemoria(self):
        tempoDic ={} # se usa un diccionario para facilitar la compatibilidad con el frontend
        for j in range(len(self.memoria)): # se toma el codigo del programa en ejecucion desde donde empieza en la memoria hasta donde termina 
            tempoDic[j] =self.memoria[j]
        return tempoDic 
    #################################################################

    
    # metodo que comprueba si es posible realizar la ejecución (la memoria debe ser mayor al kernel)
    def puedeEjecKernel(self):
        #if cantidMemo > kernel:
        if self.cantmemoria > self.kernel:
            if self.proEjec == 0:
                self.cantmemoria -= self.kernel 
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


    def cleanMemoria(self):
        self.memoria=[]