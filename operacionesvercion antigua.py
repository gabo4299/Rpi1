import pymongo
from Base import Cuarto ,Interruptor,Cortina
from itertools import chain
from collections import defaultdict
import json
cliente = pymongo.MongoClient('mongodb://localhost:27017/')


#x=Cuarto(1,'CuartoGabo','NOjet','123',1)

#coleccion.insert_one(x.toDBCollection())

class Pines:
    def __init__ (self):
        print()

    
    def BuscarPinInt(self,x):
         db = cliente["pruebaAcuarto"]
         coleccion=db["Interruptores"]
         variablepregunta={ "Pin": x}
         Encontro=0
         x=int(x)
         #print ("BUSCANDO PIN ",x)
         for var in coleccion.find({ "Pin": x },{"_id":0 , "Pin": 1 }):
             #print(var , " Es igual a ", variablepregunta)
             Encontro=Encontro+1
             break
        
         if Encontro>0:
            return True
         else:
            return False

    def BuscarPinMoto(self,x):
         db = cliente["pruebaAcuarto"]
         coleccion=db["Cortinas"]
         #variablepregunta={ "Pinmotor": x}
         Encontro=0
         x=int(x)
         
         if x<16 and x>=0:
             
            #print ("BUSCANDO PIN ",x)
             for var in coleccion.find({ "Pinmotor": x },{"_id":0 , "Pinmotor": 1 }):
                #print(var , " Es igual a ", variablepregunta)
                Encontro=Encontro+1
                break
            
             if Encontro>0:
                return True
             else:
                return False


    def BuscarPinSensor1(self,x):
         db = cliente["pruebaAcuarto"]
         coleccion=db["Cortinas"]
         #variablepregunta={ "Pinmotor": x}
         Encontro=0
         x=int(x)
         if x>=0:
            #print ("BUSCANDO PIN ",x)
            for var in coleccion.find({ "PinSensor1": x },{"_id":0 , "PinSensor1": 1 }):
                #print(var , " Es igual a ", variablepregunta)
                Encontro=Encontro+1
                return True
                break
           
            if Encontro>0:
                return True
            else:
                return False
         else :
             return ("error numero invalido")
    
    def BuscarPinSensor2(self,x):
         db = cliente["pruebaAcuarto"]
         coleccion=db["Cortinas"]
         #variablepregunta={ "Pinmotor": x}
         Encontro=0
         x=int(x)
         
         if x>=0:
            #print ("BUSCANDO PIN ",x)
            for var in coleccion.find({ "PinSensor2": x },{"_id":0 , "PinSensor2": 1 }):
                #print(var , " Es igual a ", variablepregunta)
                Encontro=Encontro+1
                
                return True
                
                break
           
            if Encontro>0:
                return True
            else:
                return False
         else :
             return ("error numero invalido")






class OpCuarto:
    def __init__ (self):
        print(" ")
    
    def buscaridcuarto(self,x):
        db = cliente["pruebaAcuarto"]
        encontro=0
        coleccion=db["Cuartos"]
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
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
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
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
        aux={}
        con =0
        for var in coleccion.find({  },{"_id":0}):
            con=con+1
            a="Cuarto"+str(con)
            aux [a] =  var["idcuarto"]
        return aux 
    def MostrarCuartoEsp(self,id):
     id=int(id)
     db = cliente["pruebaAcuarto"]
     coleccion=db["Cuartos"]
     print(id)
     for var in coleccion.find({"idcuarto": id },{"_id":0}):
        #print (var)  
        
        return var  

        
        break
     

    def insertarCuarto(self,ID,NOMBRE,FONDO,CONTRASENHA):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
        #x=input('Ingrese Id: ')
        ID=int(ID)
        if  OpCuarto().buscaridcuarto(ID)==True:
            print ("Ya existe  cuarto con este id ")
            return ("Ya existe  cuarto con este id ")
            for var in coleccion.find({ "idcuarto":ID },{"_id":0}):
                    print (var)
        else:
            print ("correcto")
            #NOMBRE=input('Ingrese Nombre: ')
            #FONDO=input ("Ingrese Fondo: ")
            #CONTRASENHA=input ("Ingrese contrasenhaa: ") '''
            cua=Cuarto(ID,NOMBRE,FONDO,CONTRASENHA,0)
            
            
            coleccion.insert_one(cua.toDBCollection())
            OpCuarto().MostrarCuartos()
            return ("Creado Satisfactoriamente")
        
                
        


        
    def eliminarCuarto(self,ID):
        db = cliente["pruebaAcuarto"]
    
        coleccion=db["Cuartos"]
        #x=input("Ingrese id:")
        ID=int(ID)
        if OpCuarto().buscaridcuarto(ID)==True:

            print("Eliminando")
            db["Interruptores"].delete_many({ "IdCuarto": ID })
            db["Cortinas"].delete_many({ "IdCuarto": ID })
            coleccion.delete_one({ "idcuarto": ID })
            OpCuarto().MostrarCuartos()
                
            
        
        else:
            print("No se encontro id")


    def modificarCuarto(self,id,paramet,valor):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
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
            
            print("El id de cuarto no existe")  

    
    
    
    
    def agregarDisp(self,id):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
        id=int(id)
        
        if OpCuarto().buscaridcuarto(id)==True:
            for va in coleccion.find({ "idcuarto" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            print(numero)
            coleccion.update_one({ "idcuarto": id}, { "$inc": { "NDispositivos": 1 } })


    def RestDisp(self,id):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cuartos"]
        id=int(id)
        
        if OpCuarto().buscaridcuarto(id)==True:
            for va in coleccion.find({ "idcuarto" : id},{ "_id": 0, "NDispositivos":{ "$slice": (-1) } }):
                numero=va
            print(numero)
            coleccion.update_one({ "idcuarto": id}, { "$inc": { "NDispositivos": -1 } })
            

   #MostrarCuartos()


    #eliminarCuarto()
    #insertarCuarto()
    #modificarCuarto()




class OpInterruptor():
    def __init__(self):
        print("")

    def MostrarInterruptores(self):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Interruptores"]
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
            db = cliente["pruebaAcuarto"]
            encontro=0
            coleccion=db["Interruptores"]
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
    def insertarInterruptor(self,IDINTERRUPTOR,IDCUARTO,PIN,DIMMER,NOMBRE):
        db = cliente["pruebaAcuarto"]
    
        #x=input('Ingrese Id Cuarto : ')
        IDCUARTO=int(IDCUARTO)
        if  OpCuarto().buscaridcuarto(IDCUARTO)==True:
            coleccion=db["Interruptores"]
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
                if Pines().BuscarPinInt(PIN)==True:
                 print('error Pin Usado')
                 return('error Pin Usado')

                else:
                    #DIMMER=input("Ingrese Si es Dimer o No: ")
                    
                    inte=Interruptor(IDINTERRUPTOR,IDCUARTO,PIN,DIMMER,'Apagado',NOMBRE)
                    coleccion.insert_one(inte.toDBCollection())
                    OpCuarto().agregarDisp(IDCUARTO)
                    OpCuarto().MostrarCuartoEsp(IDCUARTO)
                    print ("agregado satisfacctoriamente")
                    return ("agregado satisfacctoriamente")
                    
                    #OpInterruptor().MostrarInterruptores()            
        # for var in coleccion.find({ "idcuarto":x },{"_id":0}):
            #        print (var)
        else:
            print ("No existe  cuarto con este id ")
            return ("No existe  cuarto con este id ")

    def EliminarInterruptor(self,id):
        id=int(id)
        db = cliente["pruebaAcuarto"]
        coleccion=db["Interruptores"]
        if OpInterruptor().buscarIdInterruptor(id)!=0:
            
            
            for vaca in coleccion.find({ "IdInterruptor": id },{ "_id": 0, "IdCuarto": 1}):
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
            coleccion.delete_one( { "IdInterruptor": id })
            
            print("eliminado")
            OpInterruptor().MostrarInterruptores()
            OpCuarto().MostrarCuartoEsp(jsonToPython['IdCuarto'])

            
        else:
            print("no existe id de interruptor")

    def modidificarEstadoiNT(self,idInt,estado):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Interruptores"]   
        idInt=int(idInt)
        if(OpInterruptor().buscarIdInterruptor(idInt)!=0):
            coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ 'Estado': estado}})
            OpInterruptor().MostrarInterruptores()
        else:
            print("No existe Interruptor")

    def modInterruptor(self,idInt,Parametro,valor):
        
        db = cliente["pruebaAcuarto"]
        coleccion=db["Interruptores"] 
        condicion=True  
        idInt=int(idInt)
        if OpInterruptor().buscarIdInterruptor(idInt)!=0:
            for vaca in coleccion.find({ str(Parametro): {"$exists": "true" }  }):
                    condicion=False
                    if Parametro=="IdInterruptor" or Parametro=="IdCuarto" or Parametro=="Pin":
                        valor=int(valor)
                        
                        coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ str(Parametro): valor}})

                        break
                        
                    else:
                        
                        coleccion.update_one({ "IdInterruptor": idInt}, {"$set":{ str(Parametro): valor}})
                        break
            else:
                if condicion==True:
                    print("no existe parametro")
            
        else:
            print("No existe interruptor")


'''jsonData = '{"name": "Frank", "age": 39}'
print(jsonData)
jsonToPython = json.loads(jsonData)
print(jsonToPython['name'])'''#para convertir a json y despues scar un valor 

class OpCortina():
    def __init__(self):
        print () 
    def MostrarCortinas(self):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cortinas"]
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
            db = cliente["pruebaAcuarto"]
            encontro=0
            coleccion=db["Cortinas"]
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
    def insertarCortina(self,IDCORTINA,IDCUARTO,PINMOTOR,PINSENSOR1,PINSENSOR2,TIPO,NOMBRE):
        db = cliente["pruebaAcuarto"]
        PINSENSOR1=int(PINSENSOR1)
        PINSENSOR2=int(PINSENSOR2)
        #x=input('Ingrese Id Cuarto : ')
        IDCUARTO=int(IDCUARTO)
        if  OpCuarto().buscaridcuarto(IDCUARTO)==True:
            coleccion=db["Cortinas"]
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
                if Pines().BuscarPinMoto(PINMOTOR)==True:
                 print('error Pin de motor  Usado')
                 return('error Pin de motor Usado')

                else:
                    if Pines().BuscarPinSensor1(PINSENSOR1) == False and Pines().BuscarPinSensor2(PINSENSOR2) == False  :

                        # if (PINSENSOR1 != PINSENSOR2) : para evitar que sean pines iguales 
                            cor=Cortina(IDCORTINA,IDCUARTO,PINMOTOR,PINSENSOR1,PINSENSOR2,TIPO,"Abierto",NOMBRE)
                            coleccion.insert_one(cor.toDBCollection())
                            OpCuarto().agregarDisp(IDCUARTO)
                            OpCuarto().MostrarCuartoEsp(IDCUARTO)
                            OpCortina().MostrarCortinas()
                            print ("agregado")
                            return ("agregado")
                        #else:
                            #return("pines iguales")

                        
                    else :
                        print("error pines de sensores")         
                        return("error pines de sensores") 
        # for var in coleccion.find({ "idcuarto":x },{"_id":0}):
            #        print (var)
        else:
            print ("No existe  cuarto con este id ")

    def EliminarCortina(self,id):
        id=int(id)
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cortinas"]
        if OpCortina().buscarIdCortina(id)!=0:
            
            
            for vaca in coleccion.find({ "IdCortina": id },{ "_id": 0, "IdCuarto": 1}):
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
            
            print("eliminado")
            OpCortina().MostrarCortinas()
            OpCuarto().MostrarCuartoEsp(jsonToPython['IdCuarto'])

            
        else:
            print("no existe id de cortina")    

    def modidificarEstadoCortina(self,idcor,estado):
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cortinas"]   
        idcor=int(idcor)
        if(OpCortina().buscarIdCortina(idcor)!=0):
            coleccion.update_one({ "IdCortina": idcor}, {"$set":{ 'Estado': estado}})
            OpInterruptor().MostrarInterruptores()
        else:
            print("No existe Interruptor")

    def modcortina(self,idcor,Parametro,valor):
        
        db = cliente["pruebaAcuarto"]
        coleccion=db["Cortinas"] 
        condicion=True  
        idcor=int(idcor)
        if OpCortina().buscarIdCortina(idcor)!=0:
            for vaca in coleccion.find({ str(Parametro): {"$exists": "true" }  }):
                    condicion=False
                    if Parametro=="IdCortina" or Parametro=="IdCuarto" or Parametro=="Pinmotor" or Parametro=="PinSensor1" or Parametro=="PinSensor2":
                        valor=int(valor)
                        if( (Parametro== "IdCortina" and OpCortina().buscarIdCortina(valor)==0 )or (Parametro=="IdCuarto" and OpCuarto().buscaridcuarto(valor)==True) or (Parametro=="Pinmotor" and Pines().BuscarPinMoto(valor)==False) or(Parametro=="PinSensor1" and Pines().BuscarPinSensor1(valor)==False  ) or (Parametro=="PinSensor2" and Pines().BuscarPinSensor2(valor)==False)):
                            
                            coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})

                            break
                        else:
                            print('error valor' , valor)
                            break
                    else:
                        
                        coleccion.update_one({ "IdCortina": idcor}, {"$set":{ str(Parametro): valor}})
                        break
            else:
                if condicion==True:
                    print("no existe parametro")
            
        else:
            print("No existe interruptor")