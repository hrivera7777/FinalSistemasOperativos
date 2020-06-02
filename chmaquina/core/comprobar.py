from django.core.files import File

class sintax:
    leer=[] #donde se almacenan todas las instrucciones del archivo
    pantalla =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
    listaErrores =[]
    def abrirArchivo(self):
        return str(self.leer)

    ################################################################################

    ########## metodos para traer los datos de la bd necesarios para la ejecucion del archivo ###################

    def setLeer(self, leer): # introduce todas las lineas del archivo .ch
        self.leer = leer
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
        try:
            ultimaLinea = self.leer[len(self.leer)-1].rstrip().split()
            varRetorne = self.sRetorne(ultimaLinea, len(self.leer)-1)   
        except:
            ultimaLinea = ""
            varRetorne = 0
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
                    varCantRetorne +=1
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

        if varRetorne >=0:
            self.pantalla.append("no tiene retorne al final ")
            self.listaErrores.append("no tiene retorne al final ")

    #metodo para verificar si existe un error al finalizar la revision del archivo
    def hayError(self):
        ultimaLinea = len(self.leer)
        try:
            paraVerificar = self.listaErrores[-1].split()

            if paraVerificar[0]== 'Todo-ok' and int(paraVerificar[1]) == ultimaLinea:
                return False
            else:
                return True
        except:
            return True

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
    

    def clean(self):
        self.leer=[] #donde se almacenan todas las instrucciones del archivo
        self.pantalla =[] # aqui se guardaran los posibles mensajes o lo que desee mostrar (en pantalla en el frontend)
        self.listaErrores =[]