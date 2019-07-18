import time

leer=open('ConfiguracionVentana.txt','r')
estado=leer.read()
leer.close()

while estado=='SI':
    leer=open('ConfiguracionVentana.txt','r')
    estado=leer.read()
    leer.close()
    print('SI ')
    time.sleep(0.5)
else:
    exit()