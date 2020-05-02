
# import paho.mqtt.publish as publish

# s="{mesage:si}"

# publish.single("test/node", s, hostname="localhost",port=1883)
# msgs = [{'topic':"test", 'payload222':"multiple 2"},("test", "multiple 2", 0, False)]

# publish.multiple(msgs, hostname="localhost")
class Mensages:
    def __init__ (self):
        self.mES="Mensagito papa"
class Prueba:
    def __init__(self,s):

        val =''
        if s :
            val  =Mensages().mES
        else:
            val="Nega papu"
        self.ValorClase=val

    def PrintMess(self):
        print(self.ValorClase)


Prueba(True).PrintMess()