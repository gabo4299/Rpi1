# import time

# leer=open('ConfiguracionVentana.txt','r')
# estado=leer.read()
# leer.close()

# while estado=='SI':
#     leer=open('ConfiguracionVentana.txt','r')
#     estado=leer.read()
#     leer.close()
#     print('SI ')
#     time.sleep(0.5)
# else:
#     exit()

import subprocess 

proceso=subprocess.Popen(["python",''])




# import pymongo
# cliente = pymongo.MongoClient('mongodb://localhost:27017/')
# db = cliente["pruebaAcuarto2"]
# coleccion=db["Rasp"]
# paramet="PinOcupados"
# valor ={"valor":"punto","si":"no"}
# coleccion.update({ "IdRasp": 1}, {"$set":{ str(paramet): valor}},multi=True)