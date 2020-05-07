from django.core.files import File
from .models import EjecArchCh

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
    cantmemoria=int(tempo)
    tempo = tp.kernel
    kernel=int(tempo)
    ruta2.append(str(nombre2))

proEjec=len(tup2)-1 #cual programa se encuentra en ejecución  

print(ruta2)

"""
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
"""

class ejecucion:
    f = open("media/" + ruta2[proEjec], "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.readlines() #para leer linea a linea #print(leer)
    f.close()
    myfile.close()
    #estructuras de datos necesarias (se contempla leer[] y ruta2[]=>que es la lista de programas(los nombres)).
    memoria =[]
    variables =[]
    posMemVar=[]
    cantidVarixPro=[] # aqui se sabe cuantas variables son agregadas en cada uno de los programas, que representan una posicion en el arreglo 
    etiquetas =[]
    posMemEtiq=[]
    memoria.append(0) # memoria en la primera posición será el acumudador (variable requerida en el ch máquina)
    rb=[] # registro base del programa, donde empieza el programa, cada posicion corresponde a un programa (ejem rb[0] es el rb del programa 0)
    rlc =[] # registro limite del codigo, hasta donde llegan las instrucciones del programa, cada posicion corresponde a un programa (ejem rlc[0] es el rlc del programa 0) 
    rlp=[] # registro limite del programa, hasta donde llega el programa, con variables incluidas, cada posicion corresponde a un programa (ejem rlp[0] es el rlp del programa 0)

    ###############################################################################
    # necesasario para quitar el \n que se genera en algunos archivos .ch
    contadorSalto=0 # contador de salto de linea
    i=0
    contraS=""
    for i in range(len(leer)):
        contraS = leer[i] # variable para verificar si hay un salto de linea
        if contraS == str('\n'):
            contadorSalto +=1
    j=0
    for j in range(contadorSalto):
        leer.remove(str('\n'))
    ################################################################################

    #aquí se llena la memoria con el "kernel"
    i=0
    for i in range(kernel):
        memoria.append("***kernel ch***") # self.
    cantmemoria -= kernel 

    #metodo para agregar las instrucciones a la memoria 
    def agregarInstrMemoria(self, idProg):
        for i in range(len(self.leer)):
            if i==0:
                self.rb[idProg]=len(self.memoria) # para saber donde inicia el programa 
                memoria.append(self.leer[i].rstrip()) 
            elif i == len(self.leer):
                self.rlc[idProg] = len(self.memoria) # para saber donde termina el programa
                memoria.append(self.leer[i].rstrip()) 
            else:
                memoria.append(self.leer[i].rstrip()) 
            
        self.cantmemoria -= len(self.leer)
    
    #print(memoria)
    #print(cantmemoria, 'cantidad de disponible')
    #print(len(memoria))
    #variables.append('0'+'-'+'variable')
    #print(variables)
    #palabras = variables[0].split('-')
    #print(palabras)

    #metodo para saber donde inicia las instrucciones del programa en la memoria 

    def registroBase(self):
        pass


    #metodos de retorno para entregar la instrucción y su posición de memoria

    def getInstruccion(self):
        pass

    #metodo para agregar la variable a una lista con su id corresponidiente

    def varConIdProg(self, idProg, nombVar, posMemoria): # idProg > id  del programa y nombre de la variable 
        self.posMemVar.append(posMemoria) # posMemVar es global
        self.variables.append(str(idProg) + "-"+ nombVar)
        

    #metodo para identificar una linea especifica dentro de la memoria, se usará para las etiquetas 

    def encontrarLinea(self, i):
        return self.leer[i-1].rstrip()
    

    #identificar la variable en memoria

    def idenVar(self, nomVar, idProg):
        posMem = 0
        indice = 0
        for i in range(len(self.variables)-1):
            palabras = self.variables[i].split('-')
            if palabras[0]== idProg and palabras[1] == nomVar:
                indice=i

        posMem = self.posMemVar[indice]
        return posMem

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
            print('no se agregó nada nuevo')
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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt or varFloat) and (acumInt or acumFloat):
            self.memoria[0] += self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        else:
            print("error al sumar no corresponden los tipos")

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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt or varFloat) and (acumInt or acumFloat):
            self.memoria[0] -= self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        else:
            print("error al restar, no corresponden los tipos")
    
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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt or varFloat) and (acumInt or acumFloat):
            self.memoria[0] *= self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        else:
            print("error al multiplicar, no corresponden los tipos")
    

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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            self.memoria[0] /= self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        
        elif (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar == 0 or anumeroFloatVar == 0.0):
            print("error al dividir, division por Cero")
        else:
            print("error al dividir, no corresponden los tipos")
    
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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt) and (acumInt or acumFloat):
            self.memoria[0] **= self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        else:
            print("error al elevar la potencia, no corresponden los tipos")
    
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
            print('no se pudo convertir a entero la variable')
        try:
            anumeroIntAcum = int(self.memoria[0])
            acumInt = True
        except:
            acumInt = False
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real la variable')

        try:
            anumeroFloatAcum = float(self.memoria[0])
            acumFloat = True
        except:
            acumFloat = False
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar!= 0 or anumeroFloatVar != 0.0):
            self.memoria[0] %= self.memoria[self.idenVar(linea[1],idProg)] # se identifica la posicion de memoria y se trae el valor al acumulador
        
        elif (varInt or varFloat) and (acumInt or acumFloat) and (anumeroIntVar == 0 or anumeroFloatVar == 0.0):
            print("error al tomar el modulo, division por Cero")
        else:
            print("error al tomar el modulo, no corresponden los tipos")
    
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
            print('no se pudo convertir a entero el acumulador')
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
            print('no se pudo convertir a real el acumulador')
        #############################################  

        if (acumInt or acumFloat):
            self.memoria[self.idenVar(linea[1],idProg)] = abs(self.memoria[0]) # se identifica la posicion de memoria y se trae el valor al acumulador
        else:
            print("error no se puede tomar el valor absoluto, no corresponden los tipos")

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
            print("la variable 1 no es de tipo lógico")   
        
        if var2 ==0:
            var2Bol=False
        elif var2 ==1:
            var2Bol = True 
        else:
            print("la variable 2 no es de tipo lógico")  

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
            print("la variable 1 no es de tipo lógico")   
        
        if var2 ==0:
            var2Bol=False
        elif var2 ==1:
            var2Bol = True 
        else:
            print("la variable 2 no es de tipo lógico")  

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
            print("la variable 1 no es de tipo lógico")   

        self.memoria[self.idenVar(linea[2],idProg)] = not(var1Bol)
    
    def eMuestre(self, linea, idProg):
        if(linea[1]=='acumulador'):
            return self.memoria[0]
        else:
            return self.memoria[self.idenVar(linea[1],idProg)]

    def eImprima(self, linea, idProg):
        if(linea[1]=='acumulador'):
            return self.memoria[0]
        else:
            return self.memoria[self.idenVar(linea[1],idProg)]    

    def eEtiqueta(self, linea, idProg):
        
        self.etiquetas.append(linea[1]) # guardamos el nombre de la etiqueta
        instruccion = self.encontrarLinea(linea[2]) # identificamos a que instruccion se refiere la etiqu
        posMemoriaEti = 0 # variable temporal

        i=self.rb[idProg] # con esto identificamos donde inicia el programa 
        for i in range(self.rlc[idProg]): # ciclo que recorre solamente las posiciones de memoria que corresponden a las instrucciones
            if instruccion == self.memoria[i]:
                posMemoriaEti = i
                break
        self.posMemEtiq.append(posMemoriaEti) # se agrega la posicion de memoria de la instruccion a donde apunta la etiq
        
        ##esta perdiente por terminar 
        pass