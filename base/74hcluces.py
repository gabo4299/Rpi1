
def click( f1,f2,f3,f4,f5,f6,f7,f8):
    estado=0
    
    #si quieres que la salida sea como la entrada es decir que el primer lugar corresponda al 1er foco es asi
    arra=[f8,f7,f6,f5,f4,f3,f2,f1]
    #sino la salida sera al revez
    #arra=[f1,f2,f3,f4,f5,f6,f7,f8]
    
        
    for x in range(8):
     
    #  if((x+1) <= 7):
    #     #entras sin el ultimo 
    #     #  print(arra[x])
    #      if(arra[x] == 1 ):
    #         estado=1
    #         print("cambio estado ",estado)
    #         print ("presiono boton 1")
    #         if(arra[x+1]==1):
    #             print ("presiono boton 1")
    #         else:
    #             estado=0
    #             print ("presiono boton 1")
     



         if(arra[x] == 1 ):
             if(estado == arra[x]):
                 print ("presiono boton 1")
             else:
                 estado=1
                 print("#####cambio estado ",estado)
                 print ("presiono boton 1")
            
            
         if (arra[x] == 0 ):
             if(estado == arra[x]):
                 print ("presiono boton 1")
                 
             else:
                 estado=0
                 print("#####cambio estado ",estado)
                 print ("presiono boton 1")
         
                
    print("------------presiono boton 3")
     

     

# click(1,0,1,0,0,0,0,1)
click(0,1,0,0,0,1,0,0)