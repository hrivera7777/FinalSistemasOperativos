from django.core.files import File
#from io import .
from .models import ArchivosCh


#ruta=request.FILES.get('archivo')
ruta =""
tup = ArchivosCh.objects.all()
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
class sintax:
    #while(True):
    #ruta = "media/" + ruta
    #print(ruta) 
    f = open("media/" + ruta, "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.readlines() #para leer linea a linea #print(leer)
    f.close()
    myfile.close()
    
    def abrirArchivo(self):
        return str(self.leer)
    
    ################################################
    #metodo para hacer puebas de cada funcion

    def prueba(self):
        varPrueba = -2
        lista2=[]
        for i in range(len(self.leer)):
            palabras2 = self.leer[i].rstrip().split()
            varPrueba = self.sModulo(palabras2, i ,self.leer)
            if varPrueba >=0:
                concatene = "error en la linea " + str(varPrueba + 1)
                lista2.append(concatene)
            else:
                lista2.append("Todo ok")
        return lista2 
    
    """
    print(leer[0].rstrip()) # con .rstrip() se pude eliminar el salto de linea generado automaticamente.
    print(leer[1])
    """

    
    palabras = leer[0].rstrip().split()
    #print(palabras)
  
    #la letra i se usará para indicar en que linea hay un error

    #funcion para verificar si una linea comienza con un operador
    
    def iniOper(self, texto):
        #siempre debe terminar el programa con retorne, si esto no ocurre sería el problema inicial    
        ultimaLinea = texto[len(texto)].rstrip().split()
        ultimaPalabra = ultimaLinea[0]

        if ultimaLinea == "retorne":
            return len(texto)
        else:
            return -1
        i=0
        for i in range(len(leer)):
            palabras = texto[i].rstrip().split()
            operador = palabras[0]
            if operador == 'cargue':
                return i 
            elif operador == 'almacene':
                return i
            elif operador == 'vaya':
                return i
            elif operador == 'nueva':
                return i
            elif operador == 'etiqueta':
                return i
            elif operador == 'lea':
                return i
            elif operador == 'sume':
                return i
            elif operador == 'reste':
                return i
            elif operador == 'multiplique':
                return i
            elif operador == 'divida':
                return i
            elif operador == 'potencia':
                return i
            elif operador == 'modulo':
                return i
            elif operador == 'concatene':
                return i
            elif operador == 'elimine':
                return i
            elif operador == 'extraiga':
                return i
            elif operador == 'Y':
                return i
            elif operador == 'O':
                return i
            elif operador == 'NO':
                return i
            elif operador == 'muestre':
                return i
            elif operador == 'imprima':
                return i
            elif operador == 'absoluto':
                return i
            elif operador == 'vayasi':
                return i
            elif operador == '//':
                return i
            else:
                return -1
        return i
        # fin ciclo for para verificar 
    #fin funcion
    

    #funcion si existe la variable dentro del archivo ch 
    def existe(self, texto, nomVar, i): #nomVar = nombre variable 
        bandera = False
        if i==0:
            return False
        else:
            for j in range(i):
                print('buscando si existe en linea #', j+1)
                print('estamos en la linea', i+1)
                linea = texto[j].rstrip().split()
                if(linea[0]=='nueva' and linea[1]==nomVar):
                    bandera = True
                else:
                    bandera = False
            return bandera
    
    #funcion si existe la etiqueta dentro del archivo ch 
    def existeEtiq(self, texto, nomEtiq): #nomVar = nombre variable 
        for j in range(len(texto)-1):
            linea = texto[j].rstrip().split()

            if(linea[0]=='etiqueta' and linea[1]==nomEtiq):
                 return True
            else:
                return False

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
        if len(linea)==2 and linea[0] == 'alamacene' and self.existe(texto, linea[1], i): #self.existe(texto, linea[1], i)
            return -1
        else:
            return i
    
    def sVaya(self, linea, i,texto):
        if len(linea)==2 and self.existeEtiq(self, texto, linea[1]):
            return -1
        else:
            return i

    def sVayasi(self, linea, i,texto):
        if len(linea)==3 and self.existeEtiq(self, texto, linea[1]) and self.existe(self, texto, linea[2]):
            return -1
        else:
            return i

    def sNueva(self, linea, texto, i):
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
        if len(linea)==3 and bandera and linea[0] == 'etiqueta' and (anumero >=0 and anumero <= (len(texto)-1)):
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
        if len(linea)==4 and linea[0] == 'Y' and self.existe(texto, linea[1], i) and self.existe(texto, linea[2], i) and self.tipoCorrec(texto,'L',linea[1],i) and self.tipoCorrec(texto,'L',linea[2],i) and not(self.existe(texto, linea[3], i)):
            return -1
        else:
            return i

    def sO(self, linea, i,texto):
        if len(linea)==4 and linea[0] == 'O' and self.existe(texto, linea[1], i) and self.existe(texto, linea[2], i) and self.tipoCorrec(texto,'L',linea[1],i) and self.tipoCorrec(texto,'L',linea[2],i) and not(self.existe(texto, linea[3], i)):
            return -1
        else:
            return i
        
    def sNo(self, linea, i,texto):
        if len(linea)==3 and linea[0] == 'NO' and self.existe(texto, linea[1], i) and self.tipoCorrec(texto,'L',linea[1],i) and not(self.existe(texto, linea[2], i)):
            return -1
        else:
            return i

    def sMuestre(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'muestre' and self.existe(texto, linea[1], i):
            return -1
        else:
            return i

    def sImprima(self, linea, i,texto):
        if len(linea)==2 and linea[0] == 'imprima' and self.existe(texto, linea[1], i):
            return -1
        else:
            return i
            
    def sAbsoluto(self, linea, i,texto):
        if len(linea)==3 and linea[0] == 'absoluto' and self.existe(texto, linea[1], i) and (self.tipoCorrec(texto,'I',linea[1],i) or self.tipoCorrec(texto,'R',linea[1],i)) and not(self.existe(texto, linea[2], i)) :
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
        else:
            return i
        
    def sComentario(self, linea, i):
        if linea[0].find('//') == 0:
            return -1
        else:
            return i
    
    #########################################################################
    #pruba para los metodos

    j=0
    palabras2=[]
    bandera = False
    
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