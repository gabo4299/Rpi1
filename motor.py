import time
import RPi.GPIO as GPIO #Librería para controlar GPIO
GPIO.setmode(GPIO.BCM) #Simplemente nos sirve para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)
servo=20
sensorarriba=26
sensorabajo=16
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(sensorarriba, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(sensorabajo, GPIO.IN, GPIO.PUD_UP)
S=GPIO.PWM(servo,50)
S.start(7.5)
try:
    while True:
        if GPIO.input(sensorarriba)== True :
            print("sensor arriba precionado")
            S.ChangeDutyCycle(4.5) 
            time.sleep(0.5)
        else:
            if GPIO.input(sensorabajo)== True :
                print("sensor abajo precionado")
                S.ChangeDutyCycle(10.5) 
                time.sleep(0.5)
except KeyboardInterrupt:
    S.stop()
    GPIO.cleanup()
        