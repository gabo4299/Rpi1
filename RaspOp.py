
import RPi.GPIO as GPIO
from time import sleep
from adafruit_servokit import ServoKit
import adafruit_pca9685
import busio
import board
import time
class Rasp:
    def __init__(self ,Clock11,Latch12,Data14,S0,S1,S2,S3,l1,SS0,SS1,SS2,SS3,l2,CantLuces,CantPWM):
        '''Clock es el pin nro 11 del Shift que es para seleccionar que numero de pin es ,Latch es el pin 12 que sirve para mandar las datas
        del array , data es el pin 14 para cada clock tendra que ponerse un data de  0 O 1
        
        s0 , s1,s2,s3 son los primero 16 sensores ,l1 sera la lectura , lo mismo para SS y l2 
        
        CantLuces es la cantidad de luces   
        Falta Agregar la cant mot y optimizar de los sensores ! '''
        self.CantLuces=CantLuces
        if CantLuces ==8:
            self.arrayLuces=[0,0,0,0,0,0,0,0]     
        if CantLuces == 16:
            self.arrayLuces=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
        if CantLuces == 24 :
            self.arrayLuces=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if CantLuces == 32 :
            self.arrayLuces=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
     ######################### Init Luces  salidas Digitaes ############################################
        self.data_pin = Data14 #pin 14 on the 75HC595 es decir el ds2
        self.latch_pin = Latch12 #pin 12 on the 75HC595 el st set 3 
        self.clock_pin = Clock11 #pin 11 on the 75HC595 el otro 1
        if (Data14 and Latch12 and Clock11 != 0):
            GPIO.setup(Latch12, GPIO.OUT)
            GPIO.setup(Data14, GPIO.OUT)
            GPIO.setup(Clock11, GPIO.OUT)
        else:
            print("No se configuro Shift Register en esta Raspverry")

     ################################### Init Sensores lecturas Digitales  #########################################
        self.Sen0 =S0
        self.Sen1 =S1
        self.Sen2 =S2
        self.Sen3 =S3
        self.Lec1 =l1
        self.Sen20 =SS0
        self.Sen21 =SS1
        self.Sen22 =SS2
        self.Sen23 =SS3
        self.Lec2 =l2
        if (S0 and S1 and S2 and S3 and l1  != 0):
            GPIO.setup(S0, GPIO.OUT)
            GPIO.setup(S1, GPIO.OUT)
            GPIO.setup(S2, GPIO.OUT)
            GPIO.setup(S3, GPIO.OUT)
            GPIO.setup(l1, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        else:
            print("No se configuro sensores 1 Register en esta Raspverry")
        if (SS0 and SS1 and SS2 and SS3 and l2  != 0):
            GPIO.setup(SS0, GPIO.OUT)
            GPIO.setup(SS1, GPIO.OUT)
            GPIO.setup(SS2, GPIO.OUT)
            GPIO.setup(SS3, GPIO.OUT)
            GPIO.setup(l2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        else:
            print("No se configuro sensores 2 Register en esta Raspverry")
            


        ########################### INIT SERVOS #########################
        i2c = busio.I2C(board.SCL, board.SDA)
        pca = adafruit_pca9685.PCA9685(i2c)
        pca.frequency = 50
        
        
        # Set channels to the number of servo channels on your kit.
        # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
        if CantPWM != 0 : 
        
            self.kit = ServoKit(channels=CantPWM)
     
    def BitLuz (self) :
        if (self.data_pin != 0):
            estado=0
            GPIO.output(self.data_pin, False)
            arra=self.arrayLuces
            arra=arra[::-1]
            #el ::-1 es  para invertir :V 
            for x in range(self.CantLuces):    
                if(arra[x] == 1 ):
                    if(estado == arra[x]):
                        #print ("presiono boton 1")
                        GPIO.output(self.clock_pin, True)
                        #sleep(0.02)
                        GPIO.output(self.clock_pin, False)
                    else:
                        estado=1
                        GPIO.output(self.data_pin, True)
                        print("#####cambio estado ",estado)
                        #print ("presiono boton 1")
                        GPIO.output(self.clock_pin, True)
                        #sleep(0.02)
                        GPIO.output(self.clock_pin, False)
                        
                        
                if (arra[x] == 0 ):
                    if(estado == arra[x]):
                        #print ("presiono boton 1")
                        GPIO.output(self.clock_pin, True)
                        #sleep(0.02)
                        GPIO.output(self.clock_pin, False)
                            
                    else:
                        estado=0
                        GPIO.output(self.data_pin, False)
                        #print("#####cambio estado ",estado)
                        #print ("presiono boton 1")
                        GPIO.output(self.clock_pin, True)
                        #sleep(0.02)
                        GPIO.output(self.clock_pin, False)
            
            #print("------------presiono boton 3")
            GPIO.output(self.latch_pin, True)
            # sleep(0.02)
            GPIO.output(self.latch_pin, False) 
        else:
            #print("No existe Shift Register en esta Raspverry")
            return("No existe Shift Register en esta Raspverry")
    #                   EL ORDEN ES SETEAS LA LUZ  O LUCES A ENCENDER Y LUEGO ACCIONAS EL INTERRUPTOR EN ESTE CASO ACCION LUZ 
    def setLUZ(self,NPin , Estado):
        ''' Ingresas del 0 a 15 la cantidad de luces estados con 0 o 1 true false'''
        #ingresas del 1 al 16 estados con 0 o 1 true false
        NPin=int(NPin)
        
        for x in range(self.CantLuces): 
            if(x == NPin):
                if(Estado == True):
                    self.arrayLuces[x]=1
                else:
                    self.arrayLuces[x]=0

    def AccionLuz(self):
        
           print ("clock: " ,self.clock_pin, "lacht: ",self.latch_pin, "data: ",self.data_pin) 
           Rasp.BitLuz(self)

    #
    ####
    ###################sensores #################
    def Bin(self,decimal):
        decimal=decimal
        binario = [0,0,0,0]
        cont=0
        while decimal // 2 != 0 :
            binario [cont]=(decimal % 2) 
            cont=cont+1
            decimal = decimal // 2
        binario[cont]=decimal
        #print("S0 Estado :" ,binario[0] )
        #print("S1 Estado :" ,binario[1] )
        #print("S2 Estado :" ,binario[2] )
        #print("S3 Estado :" ,binario[3] )
        #print("y leer el pin tanto")
        return  binario

    
    def LeerSensor1(self,NroSen):
        if(self.Sen0 != 0):
            # print("leendo >V ")
            sen=Rasp.Bin(self,int(NroSen))            
            GPIO.output(self.Sen0, sen[0])
            GPIO.output(self.Sen1 , sen[1])
            GPIO.output(self.Sen2 , sen[2])
            GPIO.output(self.Sen3 , sen[3])
            lectura=GPIO.input(self.Lec1)
            #print (lectura)
            return (lectura)
        else:
            print("No Existe sensores 1 en esta raspberry ")
            return ("No Existe sensores 1 en esta raspberry ")

    def LeerSensor2(self,NroSen):
        if (self.Sen20 != 0) :
            # print("leendo 2 >V 

            sen=Rasp.Bin(self,int(NroSen))            
            
            GPIO.output(self.Sen20, sen[0])
            GPIO.output(self.Sen21 , sen[1])
            GPIO.output(self.Sen22 , sen[2])
            GPIO.output(self.Sen23 , sen[3])
            lectura=GPIO.input(self.Lec2)
            #print (lectura)
            return (lectura)
        else:
            print("No Existe sensores 2 en esta raspberry ")
            return("No Existe sensores 1 en esta raspberry ")

    #####################servos#################
    def MoverCortina(self,nroMot,dirc):
       ''' 
       Nmro Motor del 0 al 15
       Dirc:
       #0 = izquierda
        #1  derecha'''
       nroMot = int  (nroMot)
       dirc = int (dirc)
       if (dirc):
           self.kit.servo[nroMot].angle=0
       else:
            self.kit.servo[nroMot].angle=180
        
    def PararCortina (self,nroMot):
        nroMot = int(nroMot)
        self.kit.servo[nroMot].angle=90

 

#R=Rasp(13,19,26,14,15,18,23,24,0,0,0,0,0,16,16) #para la fecha 13 de mayo este es para el lector 1 mas cerca al final del proto 
#R=Rasp(13,19,26,14,15,18,23,24,25,8,7,1,12,16,16)
#R.setLUZ(7,0)
#R.AccionLuz()
#print ("Sensor 1")
#for x in range (16):
    #print ("Pin ",x ,"Valor : ",R.LeerSensor1(x))
#print ("\n","\n","\n")
#print ("###################")
#print ("Sensor 2")
#for x in range (16):
    #print ("Pin ",x ,"Valor : ",R.LeerSensor2(x))

#try:
    #while True  :
        #for x in range (16):
            #print ("Pin ",x ,"Valor : ",R.LeerSensor1(x))
        #sleep(0.01) 
#except KeyboardInterrupt:
    #pass


#try:
#    while True:
#        i=input ("Numero de sensor ")
#        print ("Resultado sensor ",i, " es: ",R.LeerSensor1(i))
#except KeyboardInterrupt:
#    pass


# print("Primer paasue")
# R.setLUZ(8,0)
# R.setLUZ(2,1)
# R.AccionLuz()
# sleep(1)
# print("segudno paasue")
# R.setLUZ(8,1)
# R.setLUZ(2,0)
# R.AccionLuz()
# sleep(0.5)
# print("tercer paasue")
# R.setLUZ(8,0)
# R.setLUZ(2,1)
# R.AccionLuz()
# sleep(2)
# print("4to paasue")
# R.setLUZ(8,1)
# R.setLUZ(2,1)
# R.AccionLuz()