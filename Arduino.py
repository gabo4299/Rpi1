import serial
import struct
arduino = serial.Serial('COM3', 9600,timeout=3)
if not arduino.isOpen():
    arduino.open()
cod=100
arduino.write(cod)

print (arduino.readline())
arduino.close()