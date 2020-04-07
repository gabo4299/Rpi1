from time import sleep
class Rasp:
    def __init__(self ):
        self.arrayLuces=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print ("")
    def BitLuz (self,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16) :
        estado=0
        
        #si quieres que la salida sea como la entrada es decir que el primer lugar corresponda al 1er foco es asi
        self.arrayLuces=[f16,f15,f14,f13,f12,f11,f10,f9,f8,f7,f6,f5,f4,f3,f2,f1]
        #sino la salida sera al revez
        #self.arrayLuces=[f1,f2,f3,f4,f5,f6,f7,f8]
        for x in range(16):    
            if(self.arrayLuces[x] == 1 ):
                if(estado == self.arrayLuces[x]):
                    print ("presiono boton 1")
                   
                else:
                    estado=1
                   
                    print("#####cambio estado ",estado)
                    print ("presiono boton 1")
                    
                    
                    
            if (self.arrayLuces[x] == 0 ):
                if(estado == self.arrayLuces[x]):
                    print ("presiono boton 1")
          
                        
                else:
                    estado=0
                  
                    print("#####cambio estado ",estado)
                    print ("presiono boton 1")
                   
        
        print("------------presiono boton 3")
    def setLUZ(self,NPin , Estado):
        #ingresas del 1 al 16 estados con 0 o 1 true false
        NPin=int(NPin)
        
        for x in range(16): 
            if(x+1 == NPin):
                if(Estado == True):
                    self.arrayLuces[x]=1
                else:
                    self.arrayLuces[x]=0

    def AccionLuz(self):
        for x in range(16): 
            print(self.arrayLuces[x])

        Rasp.BitLuz(self,self.arrayLuces[0],self.arrayLuces[1],self.arrayLuces[2],self.arrayLuces[3],self.arrayLuces[4],self.arrayLuces[5],self.arrayLuces[6],self.arrayLuces[7],self.arrayLuces[8],self.arrayLuces[9],self.arrayLuces[10],self.arrayLuces[11],self.arrayLuces[12],self.arrayLuces[13],self.arrayLuces[14],self.arrayLuces[15])

    


A=Rasp()

A.setLUZ(1,1)
A.setLUZ(2,1)
A.setLUZ(5,1)
A.AccionLuz()


f = True
q = int (f)

if (q):
    print (q)
