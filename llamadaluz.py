import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.cleanup()
# Definición de los pines GPIO para los LEDs
pin_led1 = 16
pin_led2 = 26
pin_led3 = 13
pin_led4 = 6

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led1, GPIO.OUT)
GPIO.setup(pin_led2, GPIO.OUT)
GPIO.setup(pin_led3, GPIO.OUT)
GPIO.setup(pin_led4, GPIO.OUT)

# Encender todos los LEDs
GPIO.output(pin_led1, GPIO.HIGH)
GPIO.output(pin_led2, GPIO.HIGH)
GPIO.output(pin_led3, GPIO.HIGH)
GPIO.output(pin_led4, GPIO.HIGH)
time.sleep(0.1)

# Juego de luces
for i in range(10):
    for pins in [
        [pin_led4],
        [pin_led4, pin_led3],
        [pin_led3, pin_led2],
        [pin_led2, pin_led1],
        [pin_led1],
    ]:
        for pin in pins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.2)
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)

# Encender todos los LEDs
GPIO.output(pin_led1, GPIO.HIGH)
GPIO.output(pin_led2, GPIO.HIGH)
GPIO.output(pin_led3, GPIO.HIGH)
GPIO.output(pin_led4, GPIO.HIGH)
time.sleep(0.1)

# Limpiar y configurar los pines GPIO antes de salir del programa
#GPIO.cleanup()