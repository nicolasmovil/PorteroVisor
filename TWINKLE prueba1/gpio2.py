import RPi.GPIO as GPIO

import time
import datetime

# Lista de GPIOs que quieres monitorear
gpios = [4, 17, 27, 22, 14, 15, 23, 24] 
#gpios = [2, 3, 4, 17, 27, 22, 14, 15, 18, 23, 24]

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

for pin in gpios:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Diccionario para almacenar el estado anterior de cada GPIO
previous_states = {pin: GPIO.HIGH for pin in gpios}

# Bucle infinito para detectar pulsaciones del botón en cada GPIO
while True:
    for pin in gpios:
        current_state = GPIO.input(pin)
        
        # Verificar si el estado del botón ha cambiado
        if current_state != previous_states[pin]:
            if current_state == GPIO.HIGH:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time} - Botón en GPIO {pin} presionado")
           # else:
            #    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           #     print(f"{current_time} - Botón en GPIO {pin} liberado")
        
        previous_states[pin] = current_state

    time.sleep(0.1)