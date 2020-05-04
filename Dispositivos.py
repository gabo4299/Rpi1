from  RaspOp  import Rasp
import RPi.GPIO as GPIO
from time import sleep
import multiprocessing

def ServoCagon(Pin,Dirc):
    if Dirc == "Arriba":
        p=GPIO.PWM(Pin,50)
        p.start(10.5)
        for i in range (0,3000):
            sleep(0.1)
    else:
        p=GPIO.PWM(Pin,50)
        p.start(4.5)
        for i in range (0,3000):
            sleep(0.1)
class Raspberry:
    def __init__ (self , IdRasp,IoT,Cant,CantPWM,BaseDeDatosRasp):
        self.IoTPins=IoT
        
        self.Id=IdRasp
        self.InfoRasp=BaseDeDatosRasp
        self.ServosFuncioando={}
        if IoT == 0 : 
            self.IoTfunc=0
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
        else : 
            if len(IoT) == 3 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],0,0,0,0,0,0,0,0,0,0,Cant,CantPWM)
            if len(IoT) == 8 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],IoT[3],IoT[4],IoT[5],IoT[6],IoT[7],0,0,0,0,0,Cant,CantPWM)
            if len(IoT) == 13 :
                self.IoTfunc = Rasp(IoT[0],IoT[1],IoT[2],IoT[3],IoT[4],IoT[5],IoT[6],IoT[7],IoT[8],IoT[9],IoT[10],IoT[11],Cant,CantPWM)
            else : 
                print ("Fatal Error IoT")
                #return ("Fatal Error IoT")


        
    def AddGpio(self,dictDePinesOcupados):
        print ("clear gpios  y despues seteas") 
        for k,v in dictDePinesOcupados.items():
            print ("lA CADENA",v, "Empieza con IoT: ","IoT" in v)
            if not "IoT" in v:
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
        self.InfoRasp=BaseDeDatosRasp
    
    def AccionLuz(self,IoTBool,Accion,Pin):
        if IoTBool :
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
        
    


class NodeMCU:
    
    def __init__(self,id,estatus):
        '''Init el Node Con el id y el estado generalmente Desactivado Para Mandar MQTTT y htpp para activarlo'''
        print ("loco no ")


#
UNO=Raspberry(0,[21,20,16],8,16,False)

UNO.AccionLuz(True,"Apagar",8)
UNO.AddGpio({2:"IoT_Si",25:"Luz",5:"PWM"})
print ("printeando :V la hueva esta esperate")
#sleep(2)
print ("ya")

#sleep(5)

UNO.AccionLuz(True,"Encender",8)
UNO.AccionMotor(False,5,"Abajo")
UNO.AccionMotor(True,0,"Abajo")
print ("izquierda")
sleep(5)
print ("DERECHA")
UNO.AccionMotor(False,5,"Arriba")
UNO.AccionMotor(True,0,"Arriba")
sleep(3)
print ("Parado")
UNO.AccionMotor(False,5,"Parar")
UNO.AccionMotor(True,0,"Parar")
