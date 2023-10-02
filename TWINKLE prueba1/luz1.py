import RPi.GPIO as GPIO
import time

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

try:
    while True:
        # Apagar todos los LEDs
        GPIO.output(pin_led1, GPIO.LOW)
        GPIO.output(pin_led2, GPIO.LOW)
        GPIO.output(pin_led3, GPIO.LOW)
        GPIO.output(pin_led4, GPIO.LOW)
        time.sleep(0.1)

        # Encender todos los LEDs
        GPIO.output(pin_led1, GPIO.HIGH)
        GPIO.output(pin_led2, GPIO.HIGH)
        GPIO.output(pin_led3, GPIO.HIGH)
        GPIO.output(pin_led4, GPIO.HIGH)
        time.sleep(0.5)

        # Apagar todos los LEDs
        GPIO.output(pin_led1, GPIO.LOW)
        GPIO.output(pin_led2, GPIO.LOW)
        GPIO.output(pin_led3, GPIO.LOW)
        GPIO.output(pin_led4, GPIO.LOW)
        time.sleep(0.1)

        # Encender todos los LEDs
        GPIO.output(pin_led1, GPIO.HIGH)
        GPIO.output(pin_led2, GPIO.HIGH)
        GPIO.output(pin_led3, GPIO.HIGH)
        GPIO.output(pin_led4, GPIO.HIGH)
        time.sleep(0.5)

        # Apagar todos los LEDs
        GPIO.output(pin_led1, GPIO.LOW)
        GPIO.output(pin_led2, GPIO.LOW)
        GPIO.output(pin_led3, GPIO.LOW)
        GPIO.output(pin_led4, GPIO.LOW)
        time.sleep(0.1)

        # Encender un LED a la vez
        for pin in [pin_led1, pin_led2, pin_led3, pin_led4]:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)

        # Encender todos los LEDs
        GPIO.output(pin_led1, GPIO.HIGH)
        GPIO.output(pin_led2, GPIO.HIGH)
        GPIO.output(pin_led3, GPIO.HIGH)
        GPIO.output(pin_led4, GPIO.HIGH)
        time.sleep(0.5)

        # Apagar todos los LEDs
        GPIO.output(pin_led1, GPIO.LOW)
        GPIO.output(pin_led2, GPIO.LOW)
        GPIO.output(pin_led3, GPIO.LOW)
        GPIO.output(pin_led4, GPIO.LOW)
        time.sleep(0.1)

        # Encender un LED a la vez en orden inverso
        for pin in [pin_led4, pin_led3, pin_led2, pin_led1]:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)

        # Encender todos los LEDs
        GPIO.output(pin_led1, GPIO.HIGH)
        GPIO.output(pin_led2, GPIO.HIGH)
        GPIO.output(pin_led3, GPIO.HIGH)
        GPIO.output(pin_led4, GPIO.HIGH)
        time.sleep(0.5)

        # Apagar todos los LEDs
        GPIO.output(pin_led1, GPIO.LOW)
        GPIO.output(pin_led2, GPIO.LOW)
        GPIO.output(pin_led3, GPIO.LOW)
        GPIO.output(pin_led4, GPIO.LOW)
        time.sleep(0.1)

        # Encender un LED a la vez, luego dos a la vez, luego tres, luego cuatro
        for pins in [
            [pin_led1],
            [pin_led1, pin_led2],
            [pin_led2, pin_led3],
            [pin_led3, pin_led4],
            [pin_led4],
        ]:
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)

except KeyboardInterrupt:
    # Limpiar los pines GPIO y finalizar el programa si se presiona Ctrl+C
    GPIO.cleanup()
