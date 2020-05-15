from django.core.files import File
#from .models import ArchivosCh, EjecArchCh

"""
#ruta=request.FILES.get('archivo')
ruta =""
#tup = ArchivosCh.objects.all() cambio de modelo para tomar la memoria y el kernel
tup = EjecArchCh.objects.all()

for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
    print(ruta)
"""
class sintax:
    

    """
    contemplado inicialmente para abrir archivos
    ruta =""
    tup = EjecArchCh.objects.all()
    nombre=""
    tp=[]
    for tp in tup:
        nombre=tp.archivo
        ruta = str(nombre)
        print(ruta)
    #while(True):
    #ruta = "media/" + ruta
    #print(ruta) 
    f=""
    myfile=""
    leer=["0 0"]*50
    #if not(tup):

    try:
        
        f = open("media/" + ruta, "r")
        myfile = File(f)
        #print(myfile)
        leer = myfile.readlines() #para leer linea a linea #print(leer)
        f.close()
        myfile.close()
    except:
        print('no se puede abrir el achivo solicitado')
    #print(leer)
    
    """
    leer=[] #donde se almacenan todas las instrucciones del archivo
    pantalla =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    listaErrores =[]
    def abrirArchivo(self):
        return str(self.leer)

    ################################################################################

    ########## metodos para traer los datos de la bd necesarios para la ejecucion del archivo ###################
    """
    def setKernel(self, kernel): # introduce cantidad de memoria del programa en ejecucion
        self.kernel=kernel

    def setCantMemo(self, cantidMemo):  # introduce la cantidad de memoria del programa en ejecucion 
        self.cantmemoria=cantidMemo
    """

    def setLeer(self, leer): # introduce todas las lineas del archivo .ch
        self.leer = leer
    
    """
    def setProgEjec(self, progEjec): # introduce el programa en ejecucion 
        self.proEjec = progEjec
    """
    #####################################################################################
    


    
    ################################################
    #metodo para hacer puebas de cada funcion

    def prueba(self):
        varPrueba = -2
        lista2=[]
        for i in range(len(self.leer)):
            palabras2 = self.leer[i].rstrip().split()
            #varPrueba = self.sModulo(palabras2, i ,self.leer)
            varPrueba = self.sVayasi(palabras2, i ,self.leer)
            if varPrueba >=0:
                concatene = "error en la linea " + str(varPrueba + 1)
                lista2.append(concatene)
            else:
                lista2.append("Todo ok " + str(i + 1))
        return lista2 
    ###########################################################################
    """
    #metodo para hacer puebas de todas las funciones juntas
    #la letra i se usará para indicar en que linea hay un error
    def pruebaTotal(self):
        varRetorne = -2 # con esta variable verificamos si existe y esta bien la ultima instruccion que es retorne
        varCantRetorne =0 
        varInstrucciones =-2 # con esta variable verificamos si existe y esta bien cada una de las instrucciones en el doc .ch 
        lista2=[] # lista donde se agregan los errores de sintaxis                      #ultimaPalabra = ultimaLinea[0]

        # necesasario para quitar el \n que se genera en algunos archivos .ch
        contadorSalto=0 # contador de salto de linea
        for i in range(len(self.leer)):
            contraS = self.leer[i] # variable para verificar si hay un salto de linea
            if contraS == str('\n'):
                contadorSalto +=1

        for j in range(contadorSalto):
            self.leer.remove(str('\n'))

        # se resta otra posición para estar en el rango de la lista creada para dividir
        ultimaLinea = self.leer[len(self.leer)-1].rstrip().split()
        varRetorne = self.sRetorne(ultimaLinea, len(self.leer)-1) 
        #print(self.leer)

        if varRetorne >=0:
            concatene = "Error, no tiene instrucción retorne al final "
            lista2.append(concatene)
            varCantRetorne +=1
        else:
            for i in range(len(self.leer)-1):

                palabras = self.leer[i].rstrip().split()
                #print(palabras)
                operador = palabras[0]
            
                if operador == 'cargue':
                    varInstrucciones = self.sCargue(palabras, i ,self.leer) 
                elif operador == 'almacene':
                    varInstrucciones = self.sAlmacene(palabras, i ,self.leer)
                elif operador == 'vaya':
                    varInstrucciones = self.sVaya(palabras, i ,self.leer)
                elif operador == 'nueva':
                    varInstrucciones = self.sNueva(palabras, i ,self.leer)
                elif operador == 'etiqueta':
                    varInstrucciones = self.sEtiqueta(palabras, i ,self.leer)
                elif operador == 'lea':
                    varInstrucciones = self.sLea(palabras, i ,self.leer)
                elif operador == 'sume':
                    varInstrucciones = self.sSume(palabras, i ,self.leer)
                elif operador == 'reste':
                    varInstrucciones = self.sReste(palabras, i ,self.leer)
                elif operador == 'multiplique':
                    varInstrucciones = self.sMultiplique(palabras, i ,self.leer)
                elif operador == 'divida':
                    varInstrucciones = self.sDivida(palabras, i ,self.leer)
                elif operador == 'potencia':
                    varInstrucciones = self.sPotencia(palabras, i ,self.leer)
                elif operador == 'modulo':
                    varInstrucciones = self.sModulo(palabras, i ,self.leer)
                elif operador == 'concatene':
                    varInstrucciones = self.sConcatene(palabras, i ,self.leer)
                elif operador == 'elimine':
                    varInstrucciones = self.sElimine(palabras, i ,self.leer)
                elif operador == 'extraiga':
                    varInstrucciones = self.sExtraiga(palabras, i ,self.leer)
                elif operador == 'Y':
                    varInstrucciones = self.sY(palabras, i ,self.leer)
                elif operador == 'O':
                    varInstrucciones = self.sO(palabras, i ,self.leer)
                elif operador == 'NO':
                    varInstrucciones = self.sNo(palabras, i ,self.leer)
                elif operador == 'muestre':
                    varInstrucciones = self.sMuestre(palabras, i ,self.leer)
                elif operador == 'imprima':
                    varInstrucciones = self.sImprima(palabras, i ,self.leer)
                elif operador == 'absoluto':
                    varInstrucciones = self.sAbsoluto(palabras, i ,self.leer)
                elif operador == 'vayasi':
                    varInstrucciones = self.sVayasi(palabras, i ,self.leer)
                elif operador == '//':
                    varInstrucciones = self.sComentario(palabras, i)
                elif operador == 'retorne':
                    varCantRetorne +=1
                else:
                    varInstrucciones = -1

                # muestra en que lienea se encuentra el error 
                if varInstrucciones >=0:
                    concatene = "error en la linea " + str(varInstrucciones + 1)
                    lista2.append(concatene)
                elif varCantRetorne > 1:
                    concatene = "se tienen más instrucciones retorne de lo necesario "
                    lista2.append(concatene)
                else:
                    lista2.append("Todo-ok " + str(i + 1))

        return lista2

    #####################fin metodo prueba total #####################################3
    """
    ############################################################################################################
    ###########################################################################################################
    

    #metodo principal para realizar la verificación de la sintaxis en el archivo

    #la letra i se usará para indicar en que linea hay un error
    def errSintax(self):
        varRetorne = -2 # con esta variable verificamos si existe y esta bien la ultima instruccion que es retorne
        varCantRetorne =0 #con esta variable se verifica si existen mas de un retorne 
        varInstrucciones =-2 # con esta variable verificamos si existe y esta bien cada una de las instrucciones en el doc .ch 

        # necesasario para quitar el \n que se genera en algunos archivos .ch
        contadorSalto=0 # contador de salto de linea
        for i in range(len(self.leer)):
            contraS = self.leer[i] # variable para verificar si hay un salto de linea
            if contraS == str('\n'):
                contadorSalto +=1

        for j in range(contadorSalto):
            self.leer.remove(str('\n'))

        # se resta otra posición para estar en el rango de la lista creada para dividir
        ultimaLinea = self.leer[len(self.leer)-1].rstrip().split()
        varRetorne = self.sRetorne(ultimaLinea, len(self.leer)-1) 
        #print(self.leer)
        """
        if varRetorne >=0:
            self.pantalla.append("Error, no tiene instrucción retorne al final ")
            varCantRetorne +=1
        else:
            -> tab
        """ 
        for i in range(len(self.leer)):

            palabras = self.leer[i].rstrip().split()
            operador = palabras[0]
            if i == len(self.leer):
                varRetorne = self.sRetorne(ultimaLinea, len(self.leer)-1)
            
            else:
                    
                if operador == 'cargue':
                    varInstrucciones = self.sCargue(palabras, i ,self.leer) 
                elif operador == 'almacene':
                    varInstrucciones = self.sAlmacene(palabras, i ,self.leer)
                elif operador == 'vaya':
                    varInstrucciones = self.sVaya(palabras, i ,self.leer)
                elif operador == 'nueva':
                    varInstrucciones = self.sNueva(palabras, i ,self.leer)
                elif operador == 'etiqueta':
                    varInstrucciones = self.sEtiqueta(palabras, i ,self.leer)
                elif operador == 'lea':
                    varInstrucciones = self.sLea(palabras, i ,self.leer)
                elif operador == 'sume':
                    varInstrucciones = self.sSume(palabras, i ,self.leer)
                elif operador == 'reste':
                    varInstrucciones = self.sReste(palabras, i ,self.leer)
                elif operador == 'multiplique':
                    varInstrucciones = self.sMultiplique(palabras, i ,self.leer)
                elif operador == 'divida':
                    varInstrucciones = self.sDivida(palabras, i ,self.leer)
                elif operador == 'potencia':
                    varInstrucciones = self.sPotencia(palabras, i ,self.leer)
                elif operador == 'modulo':
                    varInstrucciones = self.sModulo(palabras, i ,self.leer)
                elif operador == 'concatene':
                    varInstrucciones = self.sConcatene(palabras, i ,self.leer)
                elif operador == 'elimine':
                    varInstrucciones = self.sElimine(palabras, i ,self.leer)
                elif operador == 'extraiga':
                    varInstrucciones = self.sExtraiga(palabras, i ,self.leer)
                elif operador == 'Y':
                    varInstrucciones = self.sY(palabras, i ,self.leer)
                elif operador == 'O':
                    varInstrucciones = self.sO(palabras, i ,self.leer)
                elif operador == 'NO':
                    varInstrucciones = self.sNo(palabras, i ,self.leer)
                elif operador == 'muestre':
                    varInstrucciones = self.sMuestre(palabras, i ,self.leer)
                elif operador == 'imprima':
                    varInstrucciones = self.sImprima(palabras, i ,self.leer)
                elif operador == 'absoluto':
                    varInstrucciones = self.sAbsoluto(palabras, i ,self.leer)
                elif operador == 'vayasi':
                    varInstrucciones = self.sVayasi(palabras, i ,self.leer)
                elif operador == '//':
                    varInstrucciones = self.sComentario(palabras, i)
                elif operador == 'retorne':
                    #varInstrucciones = self.sRetorne(ultimaLinea, len(self.leer)-1)
                    varCantRetorne +=1
                #elif i < len(self.leer)-1 and operador == 'retorne':
                    #varCantRetorne +=1
                else:
                    varInstrucciones = -1

                # muestra en que lienea se encuentra el error 
                if varInstrucciones >=0:
                    
                    self.pantalla.append("error en la linea " + str(varInstrucciones + 1) + " " +"("+ " ".join(palabras)+")")
                    self.listaErrores.append("error en la linea " + str(varInstrucciones + 1) + " " +"("+ " ".join(palabras)+")")
                    break
                elif varCantRetorne > 1 and varRetorne >=0:
                    self.pantalla.append("se tienen más instrucciones retorne de lo necesario o no tiene retorne al final ")
                    self.listaErrores.append("se tienen más instrucciones retorne de lo necesario o no tiene retorne al final ")
                    
                    break
                else:
                    self.listaErrores.append("Todo-ok " + str(i + 1))
                    print(self.pantalla, 'esto es la pantalla')

        if varRetorne >=0:
            self.pantalla.append("no tiene retorne al final ")
            self.listaErrores.append("no tiene retorne al final ")

    #metodo para verificar si existe un error al finalizar la revision del archivo
    def hayError(self):
        ultimaLinea = len(self.leer)
        paraVerificar = self.listaErrores[-1].split()
        print(paraVerificar, 'para verificar')
        print('ultimaLinea', ultimaLinea)
    

        if paraVerificar[0]== 'Todo-ok' and int(paraVerificar[1]) == ultimaLinea:
            return False
        else:
            return True

    """
    print(leer[0].rstrip()) # con .rstrip() se pude eliminar el salto de linea generado automaticamente.
    print(leer[1])
    """

    #metodo para obtener lo que será mostrado en pantalla
    def getPantalla(self):
        return self.pantalla


    #funcion si existe la variable dentro del archivo ch 
    def existe(self, texto, nomVar, i): #nomVar = nombre variable 
        bandera = False
        if i==0:
            return False
        else:
            for j in range(i):
                #print('buscando si existe en linea #', j+1)
                #print('estamos en la linea', i+1)
                linea = texto[j].rstrip().split()
                if(linea[0]=='nueva' and linea[1]==nomVar):
                    bandera = True
                    break
                else:
                    bandera = False
            return bandera
    
    #funcion si existe la etiqueta dentro del archivo ch 
    def existeEtiq(self, texto, nomEtiq): #nomVar = nombre variable 
        bandera = False
        for j in range(len(texto)-1):
            linea = texto[j].rstrip().split()

            if(linea[0]=='etiqueta' and linea[1]==nomEtiq):
                 bandera = True
                 break
            else:
                bandera = False
        return bandera

    #funcion que verifica si el tipo de la variable es correcto
    def tipoCorrec(self, texto, tipoVar, nomVar, i):
        bandera = False 
        if i==0:
            return False
        else:
            for j in range(i):
                linea = texto[j].rstrip().split()

                if(linea[0]=='nueva' and linea[1]==nomVar and linea[2]==tipoVar):
                    bandera = True
                    break
                else:
                    bandera = False
            return bandera
    
    # funciones para verificar sintaxis de cada operador 
    ##########################################################################################
    #todos los metodos de sintaxis comienzan con s y a continuación con el nombre del operador
    
    def sCargue(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'cargue' and self.existe(texto, linea[1], i):
            return -1
        else:
            return i
        
    def sAlmacene(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'almacene' and self.existe(texto, linea[1], i): #self.existe(texto, linea[1], i)
            return -1
        else:
            return i
    
    def sVaya(self, linea, i, texto):
        if len(linea)==2 and linea[0] == 'vaya' and self.existeEtiq(texto, linea[1]):
            return -1
        else:
            return i

    def sVayasi(self, linea, i,texto):
        if len(linea)==3 and linea[0] == 'vayasi' and self.existeEtiq(texto, linea[1]) and self.existeEtiq(texto, linea[2]):
            return -1
        else:
            return i

    def sNueva(self, linea, i, texto):
        if(len(linea)==4) :
            if linea[0] == 'nueva' and not(self.existe(texto, linea[1], i)) and (linea[2] == 'C' or linea[2] == 'I' or linea[2] == 'R' or linea[2] == 'L'):
                if linea[2] == 'I':
                    anumero = 0
                    bandera = False
                    try:
                        anumero = int(linea[3])
                        bandera= True
                    except:
                        bandera= False
                        print('no se pudo convertir a entero')
                    if bandera:
                        return -1
                    else:
                        return i
                
                elif linea[2] == 'R':
                    anumero = 0.0
                    bandera = False
                    try:
                        anumero = float(linea[3])
                        bandera= True
                    except:
                        bandera= False
                        print('no se pudo convertir a real')
                    if bandera:
                        return -1
                    else:
                        return i

                elif linea[2] == 'L':
                    anumero = 2
                    bandera = False
                    try:
                        anumero = int(linea[3])
                        bandera= True
                    except:
                        bandera= False
                        print('no se pudo convertir a lógico')
                    if bandera and (anumero== 0 or anumero == 1):
                        return -1
                    else:
                        return i
                elif linea[2] == 'C':
                    return -1
                else:
                        return i       
            else:
               return i
        elif (len(linea)==3):
            if (linea[0] == 'nueva') and not(self.existe(texto, linea[1], i)) and (linea[2] == 'C' or linea[2] == 'I' or linea[2] == 'R' or linea[2] == 'L'):
                return -1
            else:
                return i    
        else:
            return i
    #fin funcion sNueva
      
    def sEtiqueta(self, linea, i,texto):
        #con este segmento convierto a int la variable si es posible 
        #####################################
        anumero = 0
        bandera = False
        try:
            anumero = int(linea[2])
            bandera= True
        except:
            bandera= False
            print('no se pudo convertir a entero')
        #############################################  
        if len(linea)==3 and bandera and linea[0] == 'etiqueta' and (anumero >=0 and anumero <= (len(texto))):
            return -1
        else:
            return i

    def sLea(self, linea, i,texto):
        if  len(linea)==2 and linea[0] == 'lea' and self.existe(texto, linea[1], i):
            return -1
        else:
            return i

    def sSume(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'sume' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):
            return -1
        else:
            return i

    def sReste(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'reste' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):
            return -1
        else:
            return i

    def sMultiplique(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'multiplique' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):
            return -1
        else:
            return i

    def sDivida(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'divida' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):
            return -1
        else:
            return i

    def sPotencia(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'potencia' and self.existe(texto, linea[1], i) and self.tipoCorrec(texto,'I',linea[1],i):
            return -1
        else:
            return i

    def sModulo(self, linea, i,texto): # puede que solo sea entero 
        if len(linea)==2 and linea[0] == 'modulo' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):
            return -1
        else:
            return i

    def sConcatene(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'concatene' and self.existe(texto, linea[1], i) and self.tipoCorrec(texto,'C',linea[1],i):
            return -1
        else:
            return i

    def sElimine(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'elimine' and self.existe(texto, linea[1], i):
            return -1
        else:
            return i

    def sExtraiga(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'extraiga' and self.existe(texto, linea[1], i) and self.tipoCorrec(texto,'I',linea[1],i):
            return -1
        else:
            return i

    def sY(self, linea, i,texto):
        if len(linea)==4 and linea[0] == 'Y' and self.existe(texto, linea[1], i) and  self.existe(texto, linea[2], i) and self.tipoCorrec(texto,'L',linea[1],i) and self.tipoCorrec(texto,'L',linea[2],i) and self.existe(texto, linea[3], i) and self.tipoCorrec(texto,'L',linea[3],i):
            return -1
        else:
            return i

    def sO(self, linea, i,texto):
        if len(linea)==4 and linea[0] == 'O' and self.existe(texto, linea[1], i) and self.existe(texto, linea[2], i) and self.tipoCorrec(texto,'L',linea[1],i) and self.tipoCorrec(texto,'L',linea[2],i) and self.existe(texto, linea[3], i) and self.tipoCorrec(texto,'L',linea[3],i):
            return -1
        else:
            return i
        
    def sNo(self, linea, i,texto):
        if len(linea)==3 and linea[0] == 'NO' and self.existe(texto, linea[1], i) and self.tipoCorrec(texto,'L',linea[1],i) and self.existe(texto, linea[2], i): # not(self.existe(texto, linea[2], i)): esta linea esta igual en las dos anteriores 
            return -1
        else:
            return i

    def sMuestre(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'muestre' and (self.existe(texto, linea[1], i) or linea[1]=='acumulador'):
            return -1
        else:
            return i

    def sImprima(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'imprima' and (self.existe(texto, linea[1], i) or linea[1]=='acumulador'):
            return -1
        else:
            return i
            
    def sAbsoluto(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'absoluto' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)):# and not(self.existe(texto, linea[2], i)) :
            return -1
        else:
            return i
    
    def sRetorne(self, linea, i):
       # print(len(linea))
       # print(linea)
        if len(linea)==2:
            #con este segmento convierto a int la variable si es posible 
            #####################################
            anumero = 0
            bandera = False
            try:
                anumero = int(linea[1])
                bandera= True
            except:
                bandera= False
                print('no se pudo convertir a entero')
            #############################################    
            if (linea[0] == 'retorne') and bandera:  #and (isinstance(anumero, (int, float)))
                return -1
            else:
                return i
        elif len(linea) == 1:
            if (linea[0] == 'retorne'):
                return -1
            else:
                return i
        else:
            return i
        
    def sComentario(self, linea, i):
        if linea[0].find('//') == 0:
            return -1
        else:
            return i
    
    ####################################################################################################################################################33
    #pruba para los metodos de manera local 
    """
    j=0
    palabras2=[]
    bandera = False

    """

    """
    #prueba for each
    for palabras2 in leer[::1]:

        palabras2.rstrip().split()
        
    """
    """
    #prueba comentario
    for j in range(len(leer)):
        palabras2 = leer[j].rstrip().split()
        if (palabras2[0].find('//') == 0):
            print(palabras2[0].find('//'), 'here')
            print (-1)
        else:
            print(palabras[0])
            print(j)
    """
    """
    #pruba metodo sRetorne
    for j in range(len(leer)):
        palabras2 = leer[j].rstrip().split()
        anumero = 0    
        try:
            anumero = int(palabras2[1])
            bandera= True
        except:
            bandera= False
            print('no se pudo convertir')
            
        if (palabras2[0] == 'retorne')  and (len(palabras2)==2 and bandera):  #and (isinstance(anumero, (int, float)))
            print ("\n",-1)
            print(type(palabras2[1]), 'if')
            print(palabras2,'if')
            print(len(palabras2), 'if')
        else:
            print(type(palabras2[1]), 'else')
            print(palabras2,'else')
            print(len(palabras2), 'else')
            print ("\n",j)

        # otra cosa diferente
        anumero = 0
        bandera = False
        try:
            anumero = int(linea[1])
            bandera= True
        except:
            bandera= False
            print('no se pudo convertir a entero')
            
        if (linea[0] == 'retorne')  and (len(linea)==2 and bandera):  #and (isinstance(anumero, (int, float)))
            return -1
        else:
            return i
        """
    """
    #prueba metodo sNueva
    anumero = 0    
    for j in range(len(leer)):
        palabras2 = leer[j].rstrip().split()
        if(len(palabras2)==4) :
                if palabras2[0] == 'nueva' and (palabras2[2] == 'C' or palabras2[2] == 'I' or palabras2[2] == 'R' or palabras2[2] == 'L'):
                    if palabras2[2] == 'I':
                        anumero = 0
                        bandera = False
                        try:
                            anumero = int(palabras2[3])
                            bandera= True
                        except:
                            bandera= False
                            print('no se pudo convertir a entero')
                        if bandera:
                            print(-1, "if tam 4 Integer") 
                        else:
                            print(j, ' else del if de 4 integer')
                    
                    elif palabras2[2] == 'R':
                        anumero = 0.0
                        bandera = False
                        try:
                            anumero = float(palabras2[3])
                            bandera= True
                        except:
                            bandera= False
                            print('no se pudo convertir a real')
                        if bandera:
                            print(-1, "if tam 4 Real")
                        else:
                            print(j, ' else del if de 4 real')

                    elif palabras2[2] == 'L':
                        anumero = 2
                        bandera = False
                        try:
                            anumero = int(palabras2[3])
                            bandera= True
                        except:
                            bandera= False
                            print('no se pudo convertir a lógico')
                        if bandera and (anumero== 0 or anumero == 1):
                            print(-1, "if tam 4 logico")
                        else:
                            print (j, ' else del if de 4 logico')       
                else:
                    print (j, ' else del if de 4 grande')
        elif (len(palabras2)==3):
            if (palabras2[0] == 'nueva') and (palabras2[2] == 'C' or palabras2[2] == 'I' or palabras2[2] == 'R' or palabras2[2] == 'L'):
                print(-1, "if tam 3")
            else:
                print(j, ' else del elif de 3')    
        else:
             print(j, ' else del if principal')
    """
    
    """
    #prueba metodo etiqueta 
    anumero = 0    
    for j in range(len(leer)):
        palabras2 = leer[j].rstrip().split()
        bandera = False
        try:
            anumero = int(palabras2[2])
            bandera= True
        except:
            bandera= False
            print('no se pudo convertir a entero')
        #############################################  
        if len(palabras2)==3 and bandera and palabras2[0] == 'etiqueta' and (anumero >=0 and anumero <= (len(leer)-1)):
            print(-1, 'if')
        else:
            print(j, 'else')
    """
    """
    for j in range(len(leer)):
        palabras2 = leer[j].rstrip().split()
        bandera = False
        if len(palabras2)==2 and palabras2[0] == 'modulo' and self.existe(leer, palabras2[1], j) and (self.tipoCorrec(leer,palabras2[1],'I',j) or self.tipoCorrec(leer,palabras2[1],'R',j)):
            print(-1, 'if')
        else:
            print(j, 'else')
    """
#print(sintax.abrirArchivo())