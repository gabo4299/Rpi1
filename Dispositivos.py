from  RaspOp  import Rasp
import RPi.GPIO as GPIO
from time import sleep
import multiprocessing
import  subprocess
import json
import os
Mesage_Control=""
def ServoCagon(Pin,Dirc):
    if Dirc == "Arriba":
        p=GPIO.PWM(Pin,50)
        p.start(10.5)
        for i in range (0,30000):
            sleep(0.1)
    else:
        p=GPIO.PWM(Pin,50)
        p.start(4.5)
        for i in range (0,30000):
            sleep(0.1)

def LecturaJson(RUTA,DircRp1,Nombre,Pin,Marca):
    cont=0
    condi=False
    StringPin='-g'+str(Pin)
    Archivo='-f'+Marca
    ####Empiezas a ahcer el irrrpy
    Lectura  = subprocess.Popen(['python', DircRp1,'-r',StringPin, Archivo,Nombre])
    while condi == False:
        with open(RUTA) as file:
            data = json.load(file)
        condi=data["Guardado"]
        cont=cont+1
        sleep(0.2)
        
        if cont >= 150:
            Mesage_Control="Time Out"
            condi=False
            break
    Lectura.kill()
    print ("Matas el proceso")
    
    
class Raspberry:
    def __init__ (self , IdRasp,IoT,Cant,CantPWM,BaseDeDatosRasp):
        self.IoTPins=IoT
        if BaseDeDatosRasp["PinesOcupados"] :
            self.AddGpio(BaseDeDatosRasp["PinesOcupados"])
        
        self.Id=IdRasp
        self.InfoRasp=BaseDeDatosRasp
        self.ServosFuncioando={}
        self.LectoresFuncionando={}
        if IoT == 0 : 
            self.IoTfunc=0
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
        else : 
            print ("el IoT es : ",IoT," COn len : ",len(IoT))
            if len(IoT) == 3 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],0,0,0,0,0,0,0,0,0,0,Cant,CantPWM)
                self.CantidadSen=0
                self.Activado= True
                print ("Completado")
                
            if len(IoT) == 8 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],IoT[3],IoT[4],IoT[5],IoT[6],IoT[7],0,0,0,0,0,Cant,CantPWM)
                self.CantidadSen=16
                self.Activado= True
                print ("Completado")
                
            if len(IoT) == 13 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],IoT[3],IoT[4],IoT[5],IoT[6],IoT[7],IoT[8],IoT[9],IoT[10],IoT[11],IoT[12],Cant,CantPWM)
                self.CantidadSen=32
                self.Activado= True
                print ("Completado")
                
            else  :
                if len(IoT) != 3 and len(IoT) != 8  and len(IoT) != 13  :
                    print ("Fatal Error IoT")
                


        
    def AddGpio(self,dictDePinesOcupados):
        
        for k,v in dictDePinesOcupados.items():
            #print ("lA CADENA",v, "Empieza con IoT: ","IoT" in v)
            if not "IoT" in v:
                print ("adicionando gṕio desde ADD GPIO , sin el IOT :",dictDePinesOcupados )
                k=int (k)
                if v == "Luz" or v == "OUTPUT":
                    GPIO.setup(k,GPIO.OUT)
                if v == "Motor" or v == "PWM":
                    GPIO.setup(k,GPIO.OUT)
                    
                if v == "Sensor" or v == "INPUT":
                    GPIO.setup(k,GPIO.IN)
                if v == "LecIR" or v == "Lector":
                    GPIO.setup(k,GPIO.IN)
                if v == "Control" or v == "IR":
                    GPIO.setup(k,GPIO.OUT)

    def AccionMotor(self ,IoTBool,Pin,Direccion):
        '''Subir Bajar ETC
        IoTBool es booleano si es true ejecuta la mierda de IoT , sino lo hace manual 
        Direccion : es Arriba 1 , Abajo 0 ,Parar 5'''
        if IoTBool:
            if Direccion == "Arriba" :
                self.IoTfunc.MoverCortina(Pin,0)
            if Direccion == "Abajo" :
                self.IoTfunc.MoverCortina(Pin,1)
            if Direccion == "Parar" :
                self.IoTfunc.PararCortina(Pin)
        else :
            
            
            #p.start(7.5)
            #p.start(1.5) # 90 grados Motor parado
            if Direccion == "Arriba" :
                
                
                if Pin not in self.ServosFuncioando.keys():
                    proceso= multiprocessing.Process(target=ServoCagon,args=(Pin,"Arriba",)) 
                    proceso.start()
                    new={Pin:proceso}
                    self.ServosFuncioando.update(new)
                else :
                    p=GPIO.PWM(Pin,50)
                    p.stop()
                    self.ServosFuncioando[Pin].terminate()
                    del self.ServosFuncioando[Pin]
                    proceso= multiprocessing.Process(target=ServoCagon,args=(Pin,"Arriba",)) 
                    proceso.start()
                    new={Pin:proceso}
                    self.ServosFuncioando.update(new)
                
            if Direccion == "Abajo" :
                if Pin not in self.ServosFuncioando.keys():
                    proceso= multiprocessing.Process(target=ServoCagon,args=(Pin,"Abajo",)) 
                    proceso.start()
                    new={Pin:proceso}
                    self.ServosFuncioando.update(new)
                else :
                    p=GPIO.PWM(Pin,50)
                    p.stop()
                    self.ServosFuncioando[Pin].terminate()
                    del self.ServosFuncioando[Pin]
                    proceso= multiprocessing.Process(target=ServoCagon,args=(Pin,"Abajo",)) 
                    proceso.start()
                    new={Pin:proceso}
                    self.ServosFuncioando.update(new)
                
            if Direccion == "Parar" :
                if Pin not in self.ServosFuncioando.keys():
                    p=GPIO.PWM(Pin,50)
                    p.stop()    
                else:
                    p=GPIO.PWM(Pin,50)
                    p.stop()
                    self.ServosFuncioando[Pin].terminate()
                    p.stop()
                    del self.ServosFuncioando[Pin]
                    
    def UpdateRaspInfo(self,Base):
        datos = self.InfoRasp ["PinesOcupados"]
        for k,v in Base.items():
            
            if not "IoT" in v :
                k=int (k)
                if v == "Luz" or v == "OUTPUT":
                    GPIO.setup(k,GPIO.OUT)
                if v == "Motor" or v == "PWM":
                    GPIO.setup(k,GPIO.OUT)
                    
                if v == "Sensor" or v == "INPUT":
                    GPIO.setup(k,GPIO.IN)
                if v == "LecIR" or v == "Lector":
                    print ("aqui va el archivo de donwloads irrp.py")
                if v == "Control" or v == "IR":
                    print ("aqui va el archivo de donwloads irrp.py")
    
    def AccionLuz(self,IoTBool,Accion,Pin):
        if IoTBool :
            print ("encendiendo desde Accion luz con IOt BOOL ,CON ESTADO" , Accion)
            if Accion == "Encender":
                
                self.IoTfunc.setLUZ(Pin ,1)

            else : 
                self.IoTfunc.setLUZ(Pin ,0)
            self.IoTfunc.AccionLuz()
        else :
            if Accion == "Encender":
                GPIO.output(Pin,True)
            else :
                GPIO.output(Pin,False)
    def LeerSensor (self,IoTBool,Pin):
        Pin=int (Pin)
        if IoTBool :
            if self.CantidadSen != 0:
                if self.CantidadSen == 16 :
                    if Pin >= (self.CantidadSen/2):
                       print (self.IoTfunc.LeerSensor1(Pin) )
                       return (self.IoTfunc.LeerSensor1(Pin) )
                    else : 
                        pin2=Pin-16
                        print (self.IoTfunc.LeerSensor2(pin2) )
                        return (self.IoTfunc.LeerSensor2(pin2) )

                else:
                    print (self.IoTfunc.LeerSensor1(Pin) )
                    return (self.IoTfunc.LeerSensor1(Pin) )
                    
                     
        else :
            return GPIO.input(Pin)
             
        
    def DoDimmer (self,Pin,Val):
        '''Valor de 0 a 100  por el momento no se puede papurri'''     
        print ("Hola :V ") 
    def BorrarCodigo(self ,Marca,Codigo):
        try:
            with open(Marca) as file:
                Cods = json.load(file) 
            if Cods[Codigo]:
                del Cods[Codigo]
                with open(Marca, 'w') as file:
                    json.dump(Cods, file)
            else:
                return("error de codigo")
        except:
            return ("error de Marca")
        
    def AddCodigo(self ,Marca,Codigo,raw):
        try:
            with open(Marca) as file:
                Cods = json.load(file) 
            if not Cods[Codigo]:
                d={Codigo:raw}
                Cods.update(d)
                with open(Marca, 'w') as file:
                    json.dump(Cods, file)
            else:
                return("error de codigo existe")
        except:
            return ("error de Marca")
    def BorrarArchivoCodigo(self ,Marca):
        try:
            os.remove(Marca)
        except:
            return ("error de Marca")
    def AddListaCompleta(self ,Marca,CodigosDict):
        try:
            with open(Marca, 'w') as file:
                    json.dump(CodigosDict, file)
        except:
            return ("error")


    def LeerCodigo(self,PIN2,Nombre,Marca):
        '''Una lecturaa a la vez  Nombre es el Nombre de Codigo y Marca es el nombre dl Archivo Donde se guardara 
        ej SAMSUNG'''
        
        RutaJson="Lector/EstadoControl.json"
        PIN2=int(PIN2)
        RutaIR="Lector/irrp_IoT_Rasp.py"
        RutaCod="Lector/"+Marca
        # compruebas el estado de la ruta 
        with open(RutaJson) as file:
            EstadoLec = json.load(file)
        if EstadoLec["Estado"]== "Desactivado":
            #inicias y lees al mismo tienpo  
            ProcessoLectura= multiprocessing.Process(target=LecturaJson,args=(RutaJson,RutaIR,Nombre,PIN2,Marca,))
            ProcessoLectura.start()
            ProcessoLectura.join()
            if Mesage_Control  == "" :
                data={
                    "Confirmado": False, 
                    "Mensaje": "", 
                    "Confirm": False, 
                    "Estado": "Desactivado", 
                    "Guardado": False}
                with open(RutaJson, 'w'  ) as file:
                    json.dump(data, file, indent=4)
                with open(RutaCod) as file:
                    CodigosNew = json.load(file)
                
                if CodigosNew[Nombre]:
                    return CodigosNew[Nombre]
                else:
                    return "Error Revise el Archivo Dispositivos .py"
            else:
                return Mesage_Control 
                
            
        else :
            return "Ocupado"

        
    def MandarCodigoIR(self,Pin,Codigo,Marca):
        StringPin= "-g"+str(Pin)
        rutaIR="Lector/irrp_IoT_Rasp.py"
        Archivo="-f"+Marca
        MandIR= subprocess.Popen(['python', rutaIR,'-p',StringPin, Archivo,Codigo])
         


class NodeMCU:
    
    def __init__(self,id,estatus):
        '''Init el Node Con el id y el estado generalmente Desactivado Para Mandar MQTTT y htpp para activarlo'''
        print ("loco no ")


#
#UNO=Raspberry(0,[21,20,16],8,16,False)

#UNO.AccionLuz(True,"Apagar",8)
#UNO.AddGpio({2:"IoT_Si",25:"Luz",5:"PWM"})

#UNO.LeerCodigo(24,"Mute","Samsung")

#UNO.MandarCodigoIR(23,"Off","Samsung")

#sleep(10)
#UNO.MandarCodigoIR(23,"Mute","Samsung")

#sleep(5)

#UNO.AccionLuz(True,"Encender",8)
#UNO.AccionMotor(False,5,"Abajo")
#UNO.AccionMotor(True,0,"Abajo")
#print ("izquierda")
#sleep(5)
#print ("DERECHA")
#UNO.AccionMotor(False,5,"Arriba")
#UNO.AccionMotor(True,0,"Arriba")
#sleep(3)
#print ("Parado")
#UNO.AccionMotor(False,5,"Parar")
#UNO.AccionMotor(True,0,"Parar")
