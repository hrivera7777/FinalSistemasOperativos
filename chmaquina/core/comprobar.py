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
    leer = myfile.readlines() #para leer linea a linea 
    #print(leer)
    f.close()
    myfile.close()
    
    def abrirArchivo(self):
        return str(self.leer)
    
    """
    print(leer[0].rstrip()) # con .rstrip() se pude eliminar el salto de linea generado automaticamente.
    print(leer[1])
    """

    # funciones para verificar sintaxis de cada operador 
    palabras = leer[0].rstrip().split()
    #print(palabras)
    
    


    #funcion para verificar si una linea comienza con un operador
    
    def iniOper(self, texto):
        #siempre debe terminar el programa con retorne, si esto no ocurre sería el problema inicial    
        ultimaLinea = texto[len(texto)].rstrip().split()
        ultimaPalabra = ultimaLinea[0]

        if ultimaLinea == "retorne":
            return len(texto)
        else:
            return -1

        
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
            else:
                return -1
        return i
        # fin ciclo for para verificar 
    #fin funcion
    
    #todos los metodos de sintaxis comienzan con s y a continuación con el nombre del operador
    
    def sCargue(self, linea):
        pass

    def sAlmacene(self, linea):
        pass
    
    def sVaya(self, linea):
        pass
    def sNueva(self, linea):
        pass
    def sEtiqueta(self, linea):
        pass
    def sLea(self, linea):
        pass
    def sSume(self, linea):
        pass
    def sReste(self, linea):
        pass
    def sMultiplique(self, linea):
        pass
    def sDivida(self, linea):
        pass
    def sPotencia(self, linea):
        pass
    def sModulo(self, linea):
        pass
    def sConcatene(self, linea):
        pass
    def sElimine(self, linea):
        pass
    def sExtraiga(self, linea):
        pass
    def sY(self, linea):
        pass
    def sO(self, linea):
        pass
    def sNo(self, linea):
        pass
    def sMuestre(self, linea):
        pass
    def sImprima(self, linea):
        pass
    def sAbsoluto(self, linea):
        pass
    def sRetorne(self, linea, i):
        if not (linea[0] == 'retorne') or not isinstance(linea[1], (int, float, complex)):  
            return -1
        else:
            return i
        

#print(sintax.abrirArchivo())