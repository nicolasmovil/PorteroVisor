import RPi.GPIO as GPIO
import time

# Configura el modo BCM para los pines GPIO
GPIO.setmode(GPIO.BCM)

# Define el nÃºmero de pin que deseas simular
pin = 11

# Configura el pin como salida
GPIO.setup(pin, GPIO.OUT)

# Simula una pulsaciÃ³n del pin durante 1 segundo
GPIO.output(pin, GPIO.HIGH)
time.sleep(1)
GPIO.output(pin, GPIO.LOW)

# Limpia la configuraciÃ³n de GPIO
GPIO.cleanup()

