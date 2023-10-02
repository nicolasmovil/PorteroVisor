import RPi.GPIO as GPIO  # Importa el módulo RPi.GPIO para controlar el GPIO
import subprocess  # Importa el módulo subprocess para ejecutar comandos en la terminal
import time  # Importa el módulo time para pausar la ejecución del programa

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)  # Configura el modo del GPIO
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura el GPIO 4 como entrada con resistencia pull-up interna

# Abre la aplicación twinkle-console utilizando Expect
print("Abriendo la aplicación twinkle-console...")
subprocess.call(["expect", "-c", 'spawn twinkle-console; sleep 3; expect "twinkle>"'])

# Bucle principal
while True:  # Inicia un bucle infinito
    if input() == "4":  # Verifica si se ha tecleado el número 4
        # Simula una pulsación del botón conectado al GPIO 4
        GPIO.add_event_detect(4, GPIO.FALLING, callback=lambda _: None, bouncetime=200)

        # Envía el comando para hacer una llamada a 101
        print("Haciendo una llamada a 101...")
       # subprocess.call(["expect", "-c", 'send "call 101\r"; sleep 30; send "bye\r"'])
        subprocess.call(["expect", "-c", 'spawn twinkle-console; sleep 3; expect "twinkle>"; send --cmd "call 101\r"; sleep 30; send --cmd "bye\r"'])

        # Espera 1 segundo para evitar rebotes del botón
        time.sleep(1)

    time.sleep(0.1)  # Espera 0.1 segundos para evitar un uso excesivo de la CPU
