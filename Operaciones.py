import pymongo
from Base import Cuarto ,Interruptor,Cortina,Casa,Control,Node,Raspberry,LecIR
from itertools import chain
from collections import defaultdict
import json
import time
cliente = pymongo.MongoClient('mongodb://localhost:27017/')

cantidadluces=16
cantidadmotores=16
cantidadsensores=32
NombreBase="pruebaAcuarto2"
#x=Cuarto(1,'CuartoGabo','NOjet','123',1)

#coleccion.insert_one(x.toDBCollection())


class OpRasp:
    def __init__ (self):
        self.CollectionName="Rasp"
        self.complete="Complete"
        self.ErrorNoId="No existe Raspberry con este  ID "
        self.ErrorIdRepetido="Ya existe  Rasp con este ID"
    def buscarRasp(self,id):
        """ Devuelve True si la Raspberry existe"""
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        encontro=0
        id=int (id)
        variablepregunta={ "IdRasp": id}
        for vaca in coleccion.find({ "IdRasp": id},{ "_id": 0, "IdRasp": 1}):
            if vaca==variablepregunta:
                encontro=1
                
                break
        
        if encontro==1:
            return True
        if encontro==0:
            return False

    def MostrarRaspEsp(self,id):
     """ Devuelve una sola Raspberry del Id especificado"""
     db = cliente[NombreBase]
     coleccion=db[self.CollectionName]
     
     for var in coleccion.find({"IdRasp": id },{"_id":0}):
          
        
        return var         
    def InsertarRasp(self,IdRasp,IdCasa,CantidadPWM,CantidadLuz,IoT):
        """ Crea Una Nueva RaspBerry , los parametros:

         PWM es variable ya que se usa una i2c de pwms que con la direccion se pueden ampliar en cascada

         la luz tambien es variabel ya que las salidas digitales se amplian mediante los 74hc595 

         Si no se tiene un IoT Escribir 0 , false

         en IoT es necesario meer una lista [] con  los pines a usar con el IoT , los pines 2 y 3  estan definidos para el I2C asi que colocar otros , minimamente 3 para las luces ,y los senosres cada 3 pines son 16 sensores
         [4,5,6] ---> solo luces la cantidad dicha 
         [4,5,6,7,8,9] ----> 16 Sensores IN """
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        IdCasa=int(IdCasa)
        allpins=[2,3,4,17,27,22,10,9,11,0,5,6,13,19,26,14,15,18,23,24,25,8,7,1,12,16,20,21]
        allpins.sort()
        
        CantidadPWM=int(CantidadPWM)
        CantidadLuz=int(CantidadLuz)
        



        if  OpRasp().buscarRasp(IdRasp)==True: 
            print (self.ErrorIdRepetido)
            return (self.ErrorIdRepetido)
        else:
            
            PinesOcupados={}
            #NOMBRE=input('Ingrese Nombre: ')
            #FONDO=input ("Ingrese Fondo: ")
            #CONTRASENHA=input ("Ingrese contrasenhaa: ") '''
            if IoT == 0:
                cua=Raspberry(IdRasp,IdCasa,allpins,PinesOcupados,len(allpins),0,0,"",0,"",0,"")
                OpCasa().agregarRasp(IdCasa)
                return (self.complete)
                
            else:
                lent=len(IoT)
                
                pinsl =[]
                pwm=[]
                sens=[]
                luz=[]
                cond=0
                cantidadsensores=0
                if lent <3 or (lent >3 and lent < 6) or (lent >6 and lent < 9):
                    print ("error en los pines de IoT")
                    return ("error en los pines de IoT")
                if lent == 3 :
                    
                    for x in range (0,cantidadsensores):
                        sens.append(x)
                    for x in range (0,CantidadPWM):
                        pwm.append(x)
                    for x in range (0,CantidadLuz):
                        luz.append(x)
                if lent == 6:
                    for x in range (0,CantidadPWM):
                        pwm.append(x)
                    for x in range (0,CantidadLuz):
                        luz.append(x)
                    cantidadsensores=16
                    for x in range (0,cantidadsensores):
                        sens.append(x)
                if lent ==9:
                    for x in range (0,CantidadPWM):
                        pwm.append(x)
                    for x in range (0,CantidadLuz):
                        luz.append(x)
                    cantidadsensores=32
                    for x in range (0,cantidadsensores):
                        sens.append(x)
                

                for x in allpins:
                    for y in IoT:
                        if y==3 or y ==2:
                            print ("error pines de PWM usados")
                            return ("error pines de PWM usados")
                        if x==y or x==2 or x==3:
                            cond=1
                        
                    if cond ==0:
                        pinsl.append(x)
                    else:
                        cond=0
                
                IoT.append(2)
                IoT.append(3)

                
                IoT.sort()
                for y in IoT:
                    PinesOcupados.update({y:"IoT"})
                
                
                cua=Raspberry(IdRasp,IdCasa,pinsl,IoT,len(pinsl),len(IoT),CantidadPWM,pwm,cantidadsensores,sens,CantidadLuz,luz)
                
            coleccion.insert_one(cua.toDBCollection())
            OpCasa().agregarRasp(IdCasa)
            return ("Creado Satisfactoriamente")            
    def ModRasp(self,id,paramet,valor):
        """ Modificas las Raspberry con el id , el paramero , y el nuevo valor """
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        condicion=True
        #x=input("Ingrese id:")
        id=int(id)
        if OpRasp().buscarRasp(id)==True:
            #y=input("Ingrese: parametro: ")

            for vaca in coleccion.find({ str(paramet): {"$exists": "true" }  }):
                #z=input('Ingrese nuevo valor pls: ')
                
                condicion=False
                if paramet=="IdRasp" or paramet=="IdCasa" or paramet=="Cantidad Pines Libres" or paramet=="Cantidad Pines Ocupados" or paramet=="Cantidad PWM" or paramet=="Cantidad Sensores" or paramet=="Cantidad Interruptores/Luces" :
                    valor=int(valor)
                    
                    coleccion.update_one({ "IdRasp": id}, {"$set":{ str(paramet): valor}})

                    
                    
                else:
                    
                    if paramet=="PinesOcupados":
                        coleccion.update({ "IdRasp": id}, {"$set":{ str(paramet): valor}},multi=True)
                    else:
                        coleccion.update_one({ "IdRasp": id}, {"$set":{ str(paramet): valor}})
                    

                
                

            else:
                if condicion==True:
                    return "No existe parametro"
                


        else:
            return("El id de casa no existe")
    def ElmiminarRasp(self,ID):
        """ Eliminas la raspberry con el Id """
        db = cliente[NombreBase]
    
        coleccion=db[self.CollectionName]
        #x=input("Ingrese id:")
        ID=int(ID)
        if OpRasp().buscarRasp(ID)==True:

            print("Eliminando")        
            coleccion.delete_one({ "IdRasp": ID })
            return("Eliminado")  
            
        
        else:
            return("No se encontro id")
    def ComprobarIoT(self,id):
        """ Devuelve True en caso de que se registro IoT en la Raspberry """
        id = int ( id )
        if OpRasp().buscarRasp(id):
            s=OpRasp().MostrarRaspEsp(id)
            if s["Cantidad PWM"] != 0 and s["Cantidad Interruptores/Luces"]!=0:
                return True
            else:
                return False
        else:
            return("No existe Rasp con este ID")

    def DevolverPinIoT(self,id,tipo):
        """ Devuelve el array de sensores de IoT de un tipo 
        Id de Raspberry 
        Tipo , IoT tiene 3 tipo Sensor , PWM (motor) y Luces (Digital Out) 
        PWM = P , p o PWM
        Sensor = S , s o sensor
        Interruptor = l , L o luz
        """
        id=int(id)
        if OpRasp().buscarRasp(id):
            if OpRasp().ComprobarIoT(id):
                s=OpRasp().MostrarRaspEsp(id)
                if tipo =="sensor" or tipo =="S" or tipo == "s":
                    if (s["Cantidad Sensores"] != 0):
                        return s["Sensores Libres"]
                    else:
                        return ("null")
                if tipo =="PWM" or tipo =="P" or tipo == "p":
                    if (s["Cantidad PWM"] != 0):
                        return s["PWM Libres"]
                    else:
                        return ("null")
                if tipo =="luz" or tipo =="L" or tipo == "l":
                    if (s["Cantidad Interruptores/Luces"] != 0):
                        return s["Interruptores/Luces Libres"]
                    else:
                        return ("null")
            else:
                return("NO EXISTE MODULO IOT")
        else:
            return ("No existe Rasp con este ID")
    def AddPinOcupadoIoT(self,id,pin,tipo):
        """ Quita del array de pines libres IoT el pin , para suponer que ese pin esta ocupado"""
        id = int (id )
        pin = int (pin)
        if OpRasp().buscarRasp(id):
            if (OpRasp().ComprobarIoT(id)):
                s=OpRasp().MostrarRaspEsp(id)
                
                if tipo =="sensor" or tipo =="S" or tipo == "s":
                    newvalue=s["Sensores Libres"]
                    for x in s["Sensores Libres"]:
                        if x == pin :
                            newvalue.remove(x)
                            break
                    if s["Cantidad Sensores"] !=0:
                        OpRasp().ModRasp(1,"Sensores Libres",newvalue)
                        
                        return("completado")
                    else:
                        return("No se registraron Sensores ")
                    
                if tipo =="PWM" or tipo =="p" or tipo == "P":
                    newvalue=s["PWM Libres"]
                    for x in s["PWM Libres"]:
                        if x == pin :
                            newvalue.remove(x)
                            break
                    OpRasp().ModRasp(1,"PWM Libres",newvalue)
                    return("completado")
                if tipo =="luz" or tipo =="l" or tipo == "L":
                    newvalue=s["Interruptores/Luces Libres"]
                    for x in s["Interruptores/Luces Libres"]:
                        if x == pin :
                            newvalue.remove(x)
                            break
                    OpRasp().ModRasp(1,"Interruptores/Luces Libres",newvalue)
                    return("completado")
                
            else:
                return ("No exixe Modulo IoT en esta Rasp")
        else:
            return("No existe Rasp con este ID")
    def BorrarPinIot(self,id,pin,tipo):
        """ anhade del array de pines libres IoT el pin , para suponer que ese pin ahora  esta libre"""
        id=int(id)
        pin=int(pin)
        if OpRasp().buscarRasp(id):
            if OpRasp().ComprobarIoT(id):
                condicion=True
                s=OpRasp().MostrarRaspEsp(id)
                if tipo =="sensor" or tipo =="S" or tipo == "s":
                    if s["Cantidad Sensores"] != 0:
                        cant =s["Cantidad Sensores"]
                        if pin in range(0,cant):
                            val=s["Sensores Libres"]
                            for x in val:
                                if x==pin:
                                    condicion=False
                                    break
                            if condicion:
                                val.append(pin)
                                val.sort()
                                OpRasp().ModRasp(1,"Sensores Libres",val)
                                return ("Completado")
                            else:
                                return ("error pin no ocupado")
                        else:
                            return ("pin fuera de rango")
                    else:
                        return ("error no se registraron sensores")
                if tipo =="PWM" or tipo =="P" or tipo == "p":
                    cant =s["Cantidad PWM"]
                    if pin in range(0,cant):
                            val=s["PWM Libres"]
                            for x in val:
                                if x==pin:
                                    condicion=False
                                    break
                            if condicion:
                                val.append(pin)
                                val.sort()
                                OpRasp().ModRasp(1,"PWM Libres",val)
                                return ("Completado")
                            else:
                                return ("error pin no ocupado")
                    else:
                            return ("pin fuera de rango")

                if tipo =="luz" or tipo =="L" or tipo == "l":
                    cant =s["Cantidad Interruptores/Luces"]
                    if pin in range(0,cant):
                            val=s["Interruptores/Luces Libres"]
                            for x in val:
                                if x==pin:
                                    condicion=False
                                    break
                            if condicion:
                                val.append(pin)
                                val.sort()
                                OpRasp().ModRasp(1,"Interruptores/Luces Libres",val)
                                return ("Completado")
                            else:
                                return ("error pin no ocupado")
                    else:
                            return ("pin fuera de rango")
                
            else:
                return ("No se registro modulo IoT en esta Rasp")
        else:
            return("No existe rasp con este ID")
    
    def DevolverPinsLibres(self,id):
        '''devuelve el array de pines libres'''
        id = int (id)
        if OpRasp().buscarRasp(id):
            R=OpRasp().MostrarRaspEsp(id)
            return R["PinesLibres"]
    
    def DevolverPinsOcupados(self,id):
         '''devuelve el dict de pines ocupados'''
         id = int (id)
         if OpRasp().buscarRasp(id):
            R=OpRasp().MostrarRaspEsp(id)
            return R["PinesOcupados"]
         else:
             return("No existe raspberry con este ID")
    def DevolverSoloPinsOcupados(self,id):
        '''devuelve el array de pines ocupados , solo pines'''
        id = int (id)
        if OpRasp().buscarRasp(id):
            R=OpRasp().DevolverPinsOcupados(id)
            lista=[]
            for k,v in R.items():
                lista.append(int(k))
            
            return lista      
    
    def AddPinOcupadoRasp(self , id,pin ,modo):
        #agregar condicions de modo
        ''' Anhade al dict de pines ocupados el pin con el modo , una descripcion el tipo de uso salida entrada etc
        con el pin como clave , y el modo como valor
        {1:in}'''
        id =int (id)
        pin = int (pin)
        if OpRasp().buscarRasp(id):
            if pin in OpRasp().DevolverPinsLibres(id):
                S=OpRasp().MostrarRaspEsp(id)
                val=OpRasp().DevolverPinsOcupados(id)
                newpines=OpRasp().DevolverPinsLibres(id)
                newpines.remove(pin)

                val.update({str(pin):modo})
                OpRasp().ModRasp(id,"PinesLibres",newpines)
                OpRasp().ModRasp(id,"PinesOcupados",val)
            else:
                return("Pin ocupado")
        else:
            return ("No existe id de Raspberry")
    
    def BorrarPinOcupadoRasp(self,id,pin):
        ''' elimina el par clave valor de la lista de ocupados, con la clave == pin '''
        id = int ( id)
        pin = int (pin)
        if OpRasp().buscarRasp(id):
            PiOc=OpRasp().DevolverPinsOcupados(id)
            PiLib=OpRasp().DevolverPinsLibres(id)
            if str(pin) in PiOc:
                    del PiOc[str(pin)]
                    PiLib.append(pin)
                    PiLib.sort()
                    OpRasp().ModRasp(id,"PinesLibres",PiLib)
                    OpRasp().ModRasp(id,"PinesOcupados",PiOc)
            else:
                return ("Pin No ocupado")
        else:
            return ("No existe id de Raspberry")
    def PinLibre(self,id,pin):
        '''Bool retorna true si el pin esta libre'''
        id =int (id)
        pin = int (pin)
        if OpRasp().buscarRasp(id):
                if pin in OpRasp().DevolverPinsLibres(id):
                    return True
                else:
                    return False
        else:
            return ("No existe Id Raspberry")
    def PinLibreIoT (self,id,pin,Tipo):
        '''Bool retorna true si el pin esta libre en el tipo de IoT'''
        id =int (id)
        pin = int (pin)
        if OpRasp().buscarRasp(id):
            if OpRasp().ComprobarIoT(id):
                if Tipo == "S" or Tipo == "s" or Tipo == "sensor":
                    if pin in OpRasp().DevolverPinIoT(id,"S"):
                        return True
                    else:
                        return False
                    
                if Tipo == "P" or Tipo == "p" or Tipo == "PWM":
                    if pin in OpRasp().DevolverPinIoT(id,"PWM"):
                        return True
                    else:
                        return False
                    
                if Tipo == "L" or Tipo == "l" or Tipo == "luz":
                    if pin in OpRasp().DevolverPinIoT(id,"luz"):
                        return True
                    else:
                        return False
            else :
                return ("Error no se Registro IoT en esta Raspberry")
                
        else:
            return ("Erro no existe ID de Raspberry")

        
# devolver pwm devolver sensores devolver i/o (luz)

#falta agregar pinocupado 
#verificarpin 
#quitar pin 

class OpNode:
    def __init__ (self):
        self.CollectionName="Node"
    def buscarNode(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        encontro=0
        id=int (id)
        variablepregunta={ "IdNode": id}
        for vaca in coleccion.find({ "IdNode": id},{ "_id": 0, "IdNode": 1}):
            if vaca==variablepregunta:
                encontro=1
                
                break
        
        if encontro==1:
            return True
        if encontro==0:
            return False
    

    def MostrarNodeEsp(self,id):
     db = cliente[NombreBase]
     coleccion=db[self.CollectionName]
     
     for var in coleccion.find({"IdNode": id },{"_id":0}):
          
        
        return var  

        
        break
    def InsertarNode(self,IdNode,IdCasa,pinLibres):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        IdCasa=int(IdCasa)
        pinLibres=int(pinLibres)
        #el node solo va poder operar INFRAROJOS , I-O , 1 analogico ,motor ,step
        if  OpNode().buscarNode(IdNode)==True: 
            print ("Ya existe  Node con este id ")
            return ("Ya existe  Node con este id ")
        else:
            
            
            cua=Node(IdNode,IdCasa,["D0","D1","D2","D3","D4","D5","D6","D7","D8"],{},pinLibres,0,"A0","",1)
            
            
            coleccion.insert_one(cua.toDBCollection())
            return ("Creado Satisfactoriamente")
    def ModNode(self,id,paramet,valor):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        condicion=True
        #x=input("Ingrese id:")
        id=int(id)
        if OpRasp().buscarRasp(id)==True:
            #y=input("Ingrese: parametro: ")

            for vaca in coleccion.find({ str(paramet): {"$exists": "true" }  }):
                #z=input('Ingrese nuevo valor pls: ')
                
                condicion=False
                if paramet=="IdNode" or paramet=="IdCasa" or paramet=="Cantidad Pines Libres" or paramet=="Cantidad Pines Ocupados" or  paramet=="Cantidad Analogicos" :
                    valor=int(valor)
                    
                    coleccion.update_one({ "IdNode": id}, {"$set":{ str(paramet): valor}})

                    
                            
                else:
                    
                    if paramet=="PinesOcupados":
                        
                        coleccion.update({ "IdNode": id}, {"$set":{ str(paramet): valor}},multi=True)
                    else:
                        coleccion.update_one({ "IdNode": id}, {"$set":{ str(paramet): valor}})
                    

                #if vaca is not None:
                #   print("ok")

            else:
                if condicion==True:
                    return "No existe parametro"
                


        else:
            
            print("El id de node no existe")
            return("El id de node no existe")
   
    def ElmiminarNode(self,ID):
        db = cliente[NombreBase]
    
        coleccion=db[self.CollectionName]
        #x=input("Ingrese id:")
        ID=int(ID)
        if OpNode().buscarNode(ID)==True:

            print("Eliminando")        
            coleccion.delete_one({ "IdNode": ID })
            return ('elimiando ')
                
            
        
        else:
            print("No se encontro id")
    def DevolverPinsLibres(self,id):
        id = int (id)
        if OpNode().buscarNode(id):
            R=OpNode().MostrarNodeEsp(id)
            return R["PinesLibres"]
        def DevolverPinsOcupados(self,id):
         id = int (id)
         if OpRasp().buscarRasp(id):
            R=OpNode().MostrarNodeEsp(id)
            return R["PinesOcupados"]
         else:
             return("No existe raspberry con este ID")
    def DevolverPinsOcupados(self,id):
         id = int (id)
         if OpNode().buscarNode(id):
            R=OpNode().MostrarNodeEsp(id)
            return R["PinesOcupados"]
         else:
             return("No existe raspberry con este ID")
    def DevolverSoloPinsOcupados(self,id):
        id = int (id)
        if OpNode().buscarNode(id):
            R=OpNode().DevolverPinsOcupados(id)
            lista=[]
            for k,v in R.items():
                lista.append(k)
            
            return lista      
    def devolverAnalogicoLibre(self,id):
        id = int (id)
        if OpNode().buscarNode(id):
            R=OpNode().MostrarNodeEsp(id)
            return R["Analogico Libre"]


    def devolverAnalogicoOcupado(self,id):
        id = int (id)
        if OpNode().buscarNode(id):
            R=OpNode().MostrarNodeEsp(id)
            return R["Analogico Ocupado"]
    def AddPinOcupadoNode(self , id,pin ,modo):
        #agregar condicions de modo
        id =int (id)
        pin = int (pin)
        if OpRasp().buscarRasp(id):
            if modo=="Analogico" or modo == "a" or modo=="A":
                if pin==0:
                    OpNode().ModNode(id,"Analogico Libre","")

                    OpNode().ModNode(id,"Analogico Ocupado","A0")
                    return ("pin Actualizado")
                else:
                    return ("pin erroneo")
                    

                
            else:
                pin="D"+str(pin)
                if pin in OpNode().DevolverPinsLibres(id):
                    S=OpNode().MostrarNodeEsp(id)
                    val=OpNode().DevolverPinsOcupados(id)
                    newpines=OpNode().DevolverPinsLibres(id)
                    newpines.remove(pin)

                    val.update({str(pin):modo})
                    OpNode().ModNode(id,"PinesLibres",newpines)
                    OpNode().ModNode(id,"PinesOcupados",val)
                else:
                    return("Pin ocupado")
        else:
            return ("No existe id de Raspberry")
    
    def BorrarPinOcupadoNode(self,id,pin,A):
        id = int ( id)
        pin = int (pin)
            
        if OpNode().buscarNode(id):
            if A:
                if pin == 0 : 
                 OpNode().ModNode(id,"Analogico Libre","A0")

                 OpNode().ModNode(id,"Analogico Ocupado","")

            else:
        
                PiOc=OpNode().DevolverPinsOcupados(id)
                PiLib=OpNode().DevolverPinsLibres(id)
                if ("D"+str(pin)) in PiOc:
                        del PiOc["D"+str(pin)]
                        PiLib.append(("D"+str(pin)))
                        OpNode().ModNode(id,"PinesLibres",PiLib)
                        OpNode().ModNode(id,"PinesOcupados",PiOc)
                else:
                    return ("Pin No ocupado")
        else:
            return ("No existe id de Node")
    def PinLibre(self,id,pin):
        id = int  ( id)
        if OpNode().buscarNode(id):
            pin="D"+str(pin)
            if pin in OpNode().DevolverPinsLibres(id):
                return True
            else:
                return False



class OpCasa:
    def __init__ (self):
        self.CollectionName="Casa"
    def buscaridcasa(self,Id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        encontro=0
        Id=int (Id)
        variablepregunta={ "IdCasa": Id}
        for vaca in coleccion.find({ "IdCasa": Id},{ "_id": 0, "IdCasa": 1}):
            if vaca==variablepregunta:
                encontro=1
                
                break
        
        if encontro==1:
            return True
        if encontro==0:
            return False
    def MostrarCasas(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        aux={"Casas":" "}
        auxdict= defaultdict(list)

        con =0
        #sort ordenar culito
        for var in (coleccion.find({  },{"_id":0}).sort("IdCasa",pymongo.ASCENDING)):
            con=con+1
            
            aux=aux.copy()
            aux.update(var)
            for k, v in chain( var.items()):
                auxdict[k].append(v)

        return auxdict 
    def MostrarIds(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        aux={}
        con =0
        for var in coleccion.find({  },{"_id":0}):
            con=con+1
            a="Cuarto"+str(con)
            aux [a] =  var["IdCasa"]
        return aux 
    def MostrarCasaEsp(self,id):
     id=int(id)
     db = cliente[NombreBase]
     coleccion=db[self.CollectionName]
     
     for var in coleccion.find({"IdCasa": id },{"_id":0}):
          
        
        return var  

        
        break

    def insertarCasa(self,IdCasa, Nombre,ip):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        IdCasa=int(IdCasa)
        if  OpCasa().buscaridcasa(IdCasa)==True: 
            print ("Ya existe  casa con este id ")
            return ("Ya existe  casa con este id ")
        else:
            
            #NOMBRE=input('Ingrese Nombre: ')
            #FONDO=input ("Ingrese Fondo: ")
            #CONTRASENHA=input ("Ingrese contrasenhaa: ") '''
            cua=Casa(IdCasa,Nombre,0,0,0,ip," ",0)
            
            
            coleccion.insert_one(cua.toDBCollection())
            return ("Creado Satisfactoriamente")


    def eliminarCasa(self,ID):
        db = cliente[NombreBase]
    
        coleccion=db[self.CollectionName]
        coleccion2=db["Cuartos"]
        #x=input("Ingrese id:")
        ID=int(ID)
        if OpCasa().buscaridcasa(ID)==True:

            print("Eliminando")
            auxdict= defaultdict(list)
            for var in (coleccion2.find({  },{"_id":0}).sort("idcasa",pymongo.ASCENDING)):
                OpCuarto().eliminarCuarto( var["idcuarto"])
                

        
            coleccion.delete_one({ "IdCasa": ID })
                
            
        
        else:
            print("No se encontro id")


    def modificarCasa(self,id,paramet,valor):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        condicion=True
        #x=input("Ingrese id:")
        id=int(id)
        if OpCasa().buscaridcasa(id)==True:
            #y=input("Ingrese: parametro: ")

            for vaca in coleccion.find({ str(paramet): {"$exists": "true" }  }):
                #z=input('Ingrese nuevo valor pls: ')
                
                condicion=False
                if paramet=="IdCasa" or paramet=="NDispositivos" or paramet=="Node" or paramet=="Rasp" :
                    valor=int(valor)
                    
                    coleccion.update_one({ "idcuarto": id}, {"$set":{ str(paramet): valor}})

                    
                    
                else:
                    
                    coleccion.update_one({ "idcuarto": id}, {"$set":{ str(paramet): valor}})
                    

                #if vaca is not None:
                #   print("ok")

            else:
                if condicion==True:
                    return "No existe parametro"
                


        else:
            
            print("El id de casa no existe")
    
    def agregarDisp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "NDispositivos": 1 } })


    def RestDisp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "NDispositivos": -1 } })
    def agregarNode(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "Node":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "Node": 1 } })


    def RestNode(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "Node":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "Node": -1 } })
    def agregarRasp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "Rasp":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "Rasp": 1 } })


    def RestRasp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "Rasp":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "Rasp": -1 } })
    def AddCuarto(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "CantidadCuartos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "CantidadCuartos": 1 } })

        
    def RestCuarto(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCasa().buscaridcasa(id)==True:
            for va in coleccion.find({ "IdCasa" : id},{ "_id": 0, "CantidadCuartos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "IdCasa": id}, { "$inc": { "CantidadCuartos": -1 } })




class OpCuarto:
    def __init__ (self):
        
        self.CollectionName="Cuartos"
    
    def buscaridcuarto(self,x):
        db = cliente[NombreBase]
        encontro=0
        coleccion=db[self.CollectionName]
        x=int(x)
        variablepregunta={ "idcuarto": x }
        for vaca in coleccion.find({ "idcuarto": x },{ "_id": 0, "idcuarto": 1}):
            if vaca==variablepregunta:
                encontro=1
                
                break
        
        if encontro==1:
            return True
        if encontro==0:
            return False
    def MostrarCuartos(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        aux={"Cuartos":" "}
        auxdict= defaultdict(list)

        con =0
        #sort ordenar culito
        for var in (coleccion.find({  },{"_id":0}).sort("idcuarto",pymongo.ASCENDING)):
            con=con+1
            
            aux=aux.copy()
            aux.update(var)
            for k, v in chain( var.items()):
                auxdict[k].append(v)

        return auxdict 
    def MostrarIds(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        aux={}
        con =0
        for var in coleccion.find({  },{"_id":0}):
            con=con+1
            a="Cuarto"+str(con)
            aux [a] =  var["idcuarto"]
        return aux 
    def MostrarCuartoEsp(self,id):
     id=int(id)
     db = cliente[NombreBase]
     coleccion=db[self.CollectionName]
     
     for var in coleccion.find({"idcuarto": id },{"_id":0}):
          
        
        return var  

        
        break
     

    def insertarCuarto(self,ID,IDCASA,NOMBRE,FONDO,CONTRASENHA):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        #x=input('Ingrese Id: ')
        ID=int(ID)
        IDCASA=int(IDCASA)
        if  OpCuarto().buscaridcuarto(ID)==True:
            print ("Ya existe  cuarto con este id ")
            return ("Ya existe  cuarto con este id ")
        else:
            
            #NOMBRE=input('Ingrese Nombre: ')
            #FONDO=input ("Ingrese Fondo: ")
            #CONTRASENHA=input ("Ingrese contrasenhaa: ") '''
            cua=Cuarto(ID,IDCASA,NOMBRE,FONDO,CONTRASENHA,0)
            
            
            coleccion.insert_one(cua.toDBCollection())
            OpCuarto().MostrarCuartos()
            OpCasa().AddCuarto(IDCASA)
            return ("Creado Satisfactoriamente")
        
                
        


        
    def eliminarCuarto(self,ID):
        db = cliente[NombreBase]
    
        coleccion=db[self.CollectionName]
        #x=input("Ingrese id:")
        ID=int(ID)
        if OpCuarto().buscaridcuarto(ID)==True:

            print("Eliminando")
            db["Interruptores"].delete_many({ "IdCuarto": ID })
            db["Cortinas"].delete_many({ "IdCuarto": ID })
            s=OpCuarto().MostrarCuartoEsp(ID)
            OpCasa().RestCuarto( s["idcasa"])
            coleccion.delete_one({ "idcuarto": ID })
            OpCuarto().MostrarCuartos()
            
            
        
        else:
            print("No se encontro id")


    def modificarCuarto(self,id,paramet,valor):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        condicion=True
        #x=input("Ingrese id:")
        id=int(id)
        if OpCuarto().buscaridcuarto(id)==True:
            #y=input("Ingrese: parametro: ")

            for vaca in coleccion.find({ str(paramet): {"$exists": "true" }  }):
                #z=input('Ingrese nuevo valor pls: ')
                
                condicion=False
                if paramet=="idcuarto" or paramet=="NDispositivos":
                    valor=int(valor)
                    
                    coleccion.update_one({ "idcuarto": id}, {"$set":{ str(paramet): valor}})

                    
                    
                else:
                    
                    coleccion.update_one({ "idcuarto": id}, {"$set":{ str(paramet): valor}})
                    

                #if vaca is not None:
                #   print("ok")

            else:
                if condicion==True:
                    return "No existe parametro"
                


        else:
            
            return("El id de cuarto no existe")  

    
    
    
    
    def agregarDisp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCuarto().buscaridcuarto(id)==True:
            for va in coleccion.find({ "idcuarto" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "idcuarto": id}, { "$inc": { "NDispositivos": 1 } })
            OpCasa().agregarDisp(OpCuarto().MostrarCuartoEsp(id)["idcasa"])
            


    def RestDisp(self,id):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        id=int(id)
        
        if OpCuarto().buscaridcuarto(id)==True:
            for va in coleccion.find({ "idcuarto" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            
            coleccion.update_one({ "idcuarto": id}, { "$inc": { "NDispositivos": -1 } })
            OpCasa().RestDisp(OpCuarto().MostrarCuartoEsp(id)["idcasa"])
            

   #MostrarCuartos()


    #eliminarCuarto()
    #insertarCuarto()
    #modificarCuarto()




class OpInterruptor:
    def __init__(self):
        
        self.CollectionName="Interruptores"

    def MostrarInterruptores(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        # aux={}
        aux={"Cuartos":" "}
        auxdict= defaultdict(list)
        # con =0
        for var in (coleccion.find({  },{"_id":0}).sort("idcuarto",pymongo.ASCENDING)):
            # con=con+1
            # a="Luz "+str(con)
            # aux [a] =  var

            aux=aux.copy()
            aux.update(var)
            for k, v in chain( var.items()):
                auxdict[k].append(v)


        # return aux
        if auxdict :
            return auxdict
        else:
            return "No Existen Luces"
            return auxdict

    def buscarIdInterruptor(self,x):
            db = cliente[NombreBase]
            encontro=0
            coleccion=db[self.CollectionName]
            x=int(x)
            #variablepregunta={ "idInterruptor": x }
            for vaca in coleccion.find({ "IdInterruptor": x },{ "_id": 0}):
                #print(vaca)
                #if vaca==variablepregunta:
                encontro=1
                    
                break
            
            if encontro>0:
                return vaca
            if encontro==0:
                return 0
    def insertarInterruptor(self,IDINTERRUPTOR,IDDISPOSITIVO,Dispositivo,IDCUARTO,PIN,DIMMER,NOMBRE):
        db = cliente[NombreBase]
        D=""
        #x=input('Ingrese Id Cuarto : ')
        IDCUARTO=int(IDCUARTO)
        IDDISPOSITIVO=int(IDDISPOSITIVO)
    
        
        if  OpCuarto().buscaridcuarto(IDCUARTO)==True:
            coleccion=db[self.CollectionName]
            if (Dispositivo=="Rasp" and OpRasp().buscarRasp(IDDISPOSITIVO))  or (Dispositivo=="Node" and OpNode().buscarNode(IDDISPOSITIVO)) or (Dispositivo == "IoT" and OpRasp().ComprobarIoT(IDDISPOSITIVO)):
        # y=input("Ingrese Id Del nuevo Interruptor: ")
                IDINTERRUPTOR=int(IDINTERRUPTOR)
                if OpInterruptor().buscarIdInterruptor(IDINTERRUPTOR)!=0:
                    print ("Ya existe Interruptor con ese Id:")
                    return ("Ya existe Interruptor con ese Id:")
                    #OpInterruptor().MostrarInterruptores()
                else:
                    #print ("llegaste aqui")
                    #z=input("Insertar Pin: ")
                    PIN=int (PIN)
                    if (Dispositivo=="Rasp" and OpRasp().PinLibre(IDDISPOSITIVO,PIN)==False)  or (Dispositivo=="Node" and OpNode().PinLibre(IDDISPOSITIVO,PIN)==False) or (Dispositivo == "IoT" and OpRasp().PinLibreIoT(IDDISPOSITIVO,PIN,"l")==False):
                        print('error Pin Usado')
                        return('error Pin Usado')

                    else:
                        if Dispositivo == "Rasp":
                            OpRasp().AddPinOcupadoRasp(IDDISPOSITIVO,PIN,"OUT")
                        if Dispositivo == "IoT":
                            OpRasp().AddPinOcupadoIoT(IDDISPOSITIVO,PIN,"l")
                        if Dispositivo == "Node":
                            OpNode().AddPinOcupadoNode(IDDISPOSITIVO,PIN,"OUT")
                        #DIMMER=input("Ingrese Si es Dimer o No: ")
                        
                        inte=Interruptor(IDINTERRUPTOR,IDCUARTO,IDDISPOSITIVO,Dispositivo,PIN,DIMMER,'Apagado',NOMBRE)
                        coleccion.insert_one(inte.toDBCollection())
                        OpCuarto().agregarDisp(IDCUARTO)
                        OpCuarto().MostrarCuartoEsp(IDCUARTO)
                        print ("agregado satisfacctoriamente")
                        return ("agregado satisfacctoriamente")
                    
                    #OpInterruptor().MostrarInterruptores()            
        # for var in coleccion.find({ "idcuarto":x },{"_id":0}):
            #        print (var)
            else:
                print("no existe dispositivo")
                return("no existe dispositivo")
        else:
            print ("No existe  cuarto con este id ")
            return ("No existe  cuarto con este id ")

    def EliminarInterruptor(self,id):
        id=int(id)
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        if OpInterruptor().buscarIdInterruptor(id)!=0:
            
            
            for vaca in coleccion.find({ "IdInterruptor": id },{ "_id": 0}):
                js=json.dumps(vaca)
                jsonToPython = json.loads(js)
                break

            OpCuarto().RestDisp(jsonToPython['IdCuarto'])
            if jsonToPython['Dispositivo'] == "Rasp":
                OpRasp().BorrarPinOcupadoRasp(jsonToPython["IdDisp"],jsonToPython["Pin"])
            if jsonToPython['Dispositivo'] == "IoT":
                OpRasp().BorrarPinIot(jsonToPython["IdDisp"],jsonToPython["Pin"],'l')
            if jsonToPython['Dispositivo'] == "Node":
                OpNode().BorrarPinOcupadoNode(jsonToPython["IdDisp"],jsonToPython["Pin"],0)            
            coleccion.delete_one( { "IdInterruptor": id })

            
            print("eliminado")
            OpInterruptor().MostrarInterruptores()
            OpCuarto().MostrarCuartoEsp(jsonToPython['IdCuarto'])

            
        else:
            print("no existe id de interruptor")
            return ("no existe dispositivo")

    def modidificarEstadoiNT(self,idInt,estado):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]   
        idInt=int(idInt)
        if(OpInterruptor().buscarIdInterruptor(idInt)!=0):
            coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ 'Estado': estado}})
            OpInterruptor().MostrarInterruptores()
        else:
            return ("No existe Interruptor")

    def modInterruptor(self,idInt,Parametro,valor):
        
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName] 
        condicion=True  
        idInt=int(idInt)
        if OpInterruptor().buscarIdInterruptor(idInt)!=0:
            for vaca in coleccion.find({ str(Parametro): {"$exists": "true" }  }):
                    condicion=False
                    if Parametro == "Dispositivo" or Parametro == "IdDisp" or Parametro=="IdCuarto":
                        return ("Error No se pueden Cambiar estos parametros , Necesita Eliminar el Dispositivo")
                    if Parametro=="IdInterruptor"  or Parametro=="Pin" :
                        valor=int(valor)
                        if Parametro=="Pin":
                                i=OpInterruptor().buscarIdInterruptor(idInt)
                                if i["Dispositivo"] == "Rasp":
                                    if OpRasp().PinLibre(i["IdDisp"],valor) == True:
                                        OpRasp().BorrarPinOcupadoRasp(i["IdDisp"],i["Pin"])
                                        OpRasp().AddPinOcupadoRasp(i["IdDisp"],valor,"OUT")
                                        
                                        return ("Complete")
                                    else:
                                        return("Error Pin Usado")

                                if i["Dispositivo"] == "IoT":
                                    if OpRasp().PinLibreIoT(i["IdDisp"],valor,"l") == True:
                                        OpRasp().BorrarPinIot(i["IdDisp"],i["Pin"],"l")
                                        OpRasp().AddPinOcupadoIoT(i["IdDisp"],valor,"l")
                                        
                                        return ("Complete")
                                    else:
                                        return("Error Pin Usado")
                                if i["Disposotivo"] == "Node":
                                    if OpNode().PinLibre(i["IdDisp"],valor) == True:
                                        OpNode().BorrarPinOcupadoNode(i["IdDisp"],i["Pin"],0)
                                        OpNode().AddPinOcupadoNode(i["IdDisp"],valor,"OUT")
                                        
                                        return ("Complete")
                                    else:
                                        return("Error Pin Usado")
                                

                                return("complete")
                        coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ str(Parametro): valor}})
                        return ("Complete")

                    else:
                            coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ str(Parametro): valor}})
                            return("complete")

                            break
                        
            else:
                if condicion==True:
                    print("no existe parametro")
                    return("no existe parametro")
            
        else:
            print("No existe interruptor")
            return("No existe interruptor")


'''jsonData = '{"name": "Frank", "age": 39}'
print(jsonData)
jsonToPython = json.loads(jsonData)
print(jsonToPython['name'])'''#para convertir a json y despues scar un valor 

class OpCortina:
    def __init__(self):
        self.CollectionName="Cortinas"
    def MostrarCortinas(self):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        # aux={}
        # con =0
        aux={"Cuartos":" "}
        auxdict= defaultdict(list)
        for var in (coleccion.find({  },{"_id":0}).sort("idcuarto",pymongo.ASCENDING)):

        #     con=con+1
        #     a="Cortina "+str(con)
        #     aux [a] =  var
        # return aux 
            ux=aux.copy()
            aux.update(var)
            for k, v in chain( var.items()):
                auxdict[k].append(v)

        return auxdict 

    def buscarIdCortina(self,x):
            db = cliente[NombreBase]
            encontro=0
            coleccion=db[self.CollectionName]
            x=int(x)
            #variablepregunta={ "idInterruptor": x }
            for vaca in coleccion.find({ "IdCortina": x },{ "_id": 0}):
                #print(vaca)
                #if vaca==variablepregunta:
                encontro=1
                    
                break
            
            if encontro>0:
                return vaca
            if encontro==0:
                return 0
    def insertarCortina(self,IDCORTINA,IDCUARTO,IDDISPOSITIVO,Dispositivo,PINMOTOR,PINSENSOR1,PINSENSOR2,TIPO,NOMBRE):
        db = cliente[NombreBase]
        PINSENSOR1=int(PINSENSOR1)
        PINSENSOR2=int(PINSENSOR2)
        #x=input('Ingrese Id Cuarto : ')
        IDCUARTO=int(IDCUARTO)
        IDDISPOSITIVO=int(IDDISPOSITIVO)
        if (Dispositivo=="Rasp" and OpRasp().buscarRasp(IDDISPOSITIVO))  or (Dispositivo=="Node" and OpNode().buscarNode(IDDISPOSITIVO)) or (Dispositivo=="IoT" and OpRasp().ComprobarIoT(IDDISPOSITIVO)) :
            if  OpCuarto().buscaridcuarto(IDCUARTO)==True:
                coleccion=db[self.CollectionName]
            # y=input("Ingrese Id Del nuevo Interruptor: ")
                IDCORTINA=int(IDCORTINA)
                if OpCortina().buscarIdCortina(IDCORTINA)!=0:
                    print ("Ya existe cortina con ese Id:")
                    return ("Ya existe cortina con ese Id:")
                    #OpCortina().MostrarCortinas()
                else:
                    #print ("llegaste aqui")
                    #z=input("Insertar Pin: ")
                    PINMOTOR=int (PINMOTOR)
                    if (Dispositivo=="Rasp" and OpRasp().PinLibre(IDDISPOSITIVO,PINMOTOR)==False)  or (Dispositivo=="Node" and OpNode().PinLibre(IDDISPOSITIVO,PINMOTOR)==False) or (Dispositivo == "IoT" and OpRasp().PinLibreIoT(IDDISPOSITIVO,PINMOTOR,"PWM")==False):
                        print('error Pin de motor  Usado')
                        return('error Pin de motor Usado')

                    else:
                        if Dispositivo=="Rasp" :
                            ListSen=OpRasp().DevolverPinsLibres(IDDISPOSITIVO)
                        if Dispositivo=="IoT" :
                            ListSen=OpRasp().DevolverPinIoT(IDDISPOSITIVO,"s")
                        if Dispositivo=="Node" :
                            ListSen=OpNode().DevolverPinsLibres(IDDISPOSITIVO)
                        if (PINSENSOR1 in ListSen ) and (PINSENSOR1 != PINSENSOR2 ) and (PINSENSOR2 in ListSen) :

                            # if (PINSENSOR1 != PINSENSOR2) : para evitar que sean pines iguales 
                                cor=Cortina(IDCORTINA,IDCUARTO,IDDISPOSITIVO,Dispositivo, PINMOTOR,PINSENSOR1,PINSENSOR2,TIPO,"Abierto",NOMBRE)
                                coleccion.insert_one(cor.toDBCollection())
                                OpCuarto().agregarDisp(IDCUARTO)
                                OpCuarto().MostrarCuartoEsp(IDCUARTO)
                                OpCortina().MostrarCortinas()
                                if Dispositivo=="Rasp" :
                                    OpRasp().AddPinOcupadoRasp(IDDISPOSITIVO,PINSENSOR1,"IN")
                                    OpRasp().AddPinOcupadoRasp(IDDISPOSITIVO,PINSENSOR2,"IN")
                                    OpRasp().AddPinOcupadoRasp(IDDISPOSITIVO,PINMOTOR,"PWM")
                                if Dispositivo=="IoT" :
                                     OpRasp().AddPinOcupadoIoT(IDDISPOSITIVO,PINSENSOR1,"S")
                                     OpRasp().AddPinOcupadoIoT(IDDISPOSITIVO,PINSENSOR2,"S")
                                     OpRasp().AddPinOcupadoIoT(IDDISPOSITIVO,PINMOTOR,"PWM")
                                if Dispositivo=="Node" :
                                    OpNode().AddPinOcupadoNode(IDDISPOSITIVO,PINSENSOR1,"IN")
                                    OpNode().AddPinOcupadoNode(IDDISPOSITIVO,PINSENSOR2,"IN")
                                    OpNode().AddPinOcupadoNode(IDDISPOSITIVO,PINMOTOR,"PWM")
                                print ("Agregado Safisfactoriamente")
                                return ("Agregado Safisfactoriamente")
                            #else:
                                #return("pines iguales")

                            
                        else :
                            print("error pines de sensores")         
                            return("error pines de sensores") 
            # for var in coleccion.find({ "idcuarto":x },{"_id":0}):
                #        print (var)
            
            else:
                print ("No existe  cuarto con este id ")
        else:
            print ("NO EXISTE Dispositivo")

    def EliminarCortina(self,id):
        id=int(id)
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]
        if OpCortina().buscarIdCortina(id)!=0:
            
            
            for vaca in coleccion.find({ "IdCortina": id },{ "_id": 0,}):
                #print(vaca)
                #if vaca==variablepregunta:
                js=json.dumps(vaca)
                jsonToPython = json.loads(js)
                #print("el json to python seria ",jsonToPython['IdCuarto'])
                #input()
                #agg=''.join(map(str, jsonToPython['IdCuarto']))
                #print(agg)
                break
            OpCuarto().RestDisp(jsonToPython['IdCuarto'])
            coleccion.delete_one( { "IdCortina": id })
            if jsonToPython['Dispositivo'] == "Rasp":
                OpRasp().BorrarPinOcupadoRasp(jsonToPython["IdDisp"],jsonToPython["Pinmotor"])
                OpRasp().BorrarPinOcupadoRasp(jsonToPython["IdDisp"],jsonToPython["PinSensor1"])
                OpRasp().BorrarPinOcupadoRasp(jsonToPython["IdDisp"],jsonToPython["PinSensor2"])
            if jsonToPython['Dispositivo'] == "IoT":
                OpRasp().BorrarPinIot(jsonToPython["IdDisp"],jsonToPython["Pinmotor"],'PWM')
                OpRasp().BorrarPinIot(jsonToPython["IdDisp"],jsonToPython["PinSensor1"],'s')
                OpRasp().BorrarPinIot(jsonToPython["IdDisp"],jsonToPython["PinSensor2"],'s')
            if jsonToPython['Dispositivo'] == "Node":
                OpNode().BorrarPinOcupadoNode(jsonToPython["IdDisp"],jsonToPython["Pinmotor"],0) 
                OpNode().BorrarPinOcupadoNode(jsonToPython["IdDisp"],jsonToPython["PinSensor1"],0) 
                OpNode().BorrarPinOcupadoNode(jsonToPython["IdDisp"],jsonToPython["PinSensor2"],0) 

            print("eliminado")
            OpCortina().MostrarCortinas()
            OpCuarto().MostrarCuartoEsp(jsonToPython['IdCuarto'])

            
        else:
            print("no existe id de cortina")    

    def modidificarEstadoCortina(self,idcor,estado):
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName]   
        idcor=int(idcor)
        if(OpCortina().buscarIdCortina(idcor)!=0):
            coleccion.update_one({ "IdCortina": idcor}, {"$set":{ 'Estado': estado}})
            OpInterruptor().MostrarInterruptores()
        else:
            print("No existe Interruptor")

    def modcortina(self,idcor,Parametro,valor):
        
        db = cliente[NombreBase]
        coleccion=db[self.CollectionName] 
        condicion=True  
        idcor=int(idcor)
        if OpCortina().buscarIdCortina(idcor)!=0:
            for vaca in coleccion.find({ str(Parametro): {"$exists": "true" }  }):
                    condicion=False
                    cort=OpCortina().buscarIdCortina(idcor)
                    if Parametro == "IdDisp" or Parametro == "Dispositivo" or Parametro=="IdCuarto":
                        return ("Error no se puede cambiar parametro, es necesario Eliminar El Dispositivo")
                    if Parametro=="IdCortina" or Parametro=="Pinmotor" or Parametro=="PinSensor1" or Parametro=="PinSensor2" or Parametro=="IdDispositivo":
                        valor=int(valor)
                        if( (Parametro== "IdCortina" and OpCortina().buscarIdCortina(valor)==0 ) or (Parametro=="IdCuarto" and OpCuarto().buscaridcuarto(valor)==True))  :
                            
                            coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})

                            return ("Completado")
                            break
                        if cort["Dispositivo"] == "Rasp":
                                if (Parametro=="Pinmotor" and OpRasp().PinLibre(cort["IdDisp"],valor)==True):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["Pinmotor"])
                                    OpRasp().AddPinOcupadoRasp(cort["IdDisp"],valor,"PWM")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor1" and OpRasp().PinLibre(cort["IdDisp"],valor)==True ):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["PinSensor1"])
                                    OpRasp().AddPinOcupadoRasp(cort["IdDisp"],valor,"IN")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor2" and OpRasp().PinLibre(cort["IdDisp"],valor)==True):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["PinSensor2"])
                                    OpRasp().AddPinOcupadoRasp(cort["IdDisp"],valor,"IN")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                else:
                                    return("Error pin ocupado")
                        if cort["Dispositivo"] == "IoT":
                                if (Parametro=="Pinmotor" and OpRasp().PinLibreIoT(cort["IdDisp"],valor,"PWM")==True):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["Pinmotor"])
                                    OpRasp().AddPinOcupadoIoT(cort["IdDisp"],valor,"PWM")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor1" and OpRasp().PinLibreIoT(cort["IdDisp"],valor,"S")==True):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["PinSensor1"])
                                    OpRasp().AddPinOcupadoIoT(cort["IdDisp"],valor,"S")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor2" and OpRasp().PinLibreIoT(cort["IdDisp"],valor,"S")==True):
                                    OpRasp().BorrarPinOcupadoRasp(cort["IdDisp"],cort["PinSensor1"])
                                    OpRasp().AddPinOcupadoIoT(cort["IdDisp"],valor,"S")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                else:
                                    return("Error pin ocupado")
                        if cort["Dispositivo"] == "Node":
                                if (Parametro=="Pinmotor" and OpNode().PinLibre(cort["IdDisp"],valor)==True):
                                    OpNode().BorrarPinOcupadoNode(cort["IdDisp"],cort["Pinmotor"],0)
                                    OpNode().AddPinOcupadoNode(cort["IdDisp"],valor,"PWM")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor1" and OpNode().PinLibre(cort["IdDisp"],valor)==True):
                                    OpNode().BorrarPinOcupadoNode(cort["IdDisp"],cort["PinSensor1"],0)
                                    OpNode().AddPinOcupadoNode(cort["IdDisp"],valor,"IN")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                if (Parametro=="PinSensor2" and OpNode().PinLibre(cort["IdDisp"],valor)==True):
                                    OpNode().BorrarPinOcupadoNode(cort["IdDisp"],cort["PinSensor2"],0)
                                    OpNode().AddPinOcupadoNode(cort["IdDisp"],valor,"IN")
                                    coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                                    return ("Completado")
                                    break
                                else:
                                    return("Error pin ocupado")
                        else:                                
                            print('error valor' , valor)
                            break
                    else:
                        
                        coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                        break
            else:
                if condicion==True:
                    return("no existe parametro")
            
        else:
            return("No existe interruptor")
'''OpCuarto().MostrarCuartos()
OpCortina().EliminarCortina(2)
input()

#OpCortina().insertarCortina(1,2,17,1,2,'roler')

input()
OpCortina().modcortina(1,'Pinmotor',0)
OpCortina().MostrarCortinas()'''
# class oOSonos:,class OpRF:,class OpControl:,class OpTemp:,  FALTA TODO ESTO 


# OpCasa().insertarCasa(1,"Gabo",124.11)
# OpRasp().InsertarRasp(1,1,16,16,[1,0,4,5,6,7])
# OpCuarto().insertarCuarto(1,1,"gABOS","","")
# OpInterruptor().insertarInterruptor(1,1,"IoT",1,5,"No","principal")

# OpCortina().insertarCortina(1,1,1,"IoT",4,6,9,"Roller","Derecha")

# OpCortina().EliminarCortina(1)
# OpInterruptor().EliminarInterruptor(1)
print (OpInterruptor().modInterruptor(1,"Pin",0))
print (OpInterruptor().modidificarEstadoiNT(1,"Encendido"))
# OpRasp().BorrarPinIot(1,5,"l")




#solo faltaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  radio control , ventana , infrarojos , database de infrarojos ,sensor temp,etc