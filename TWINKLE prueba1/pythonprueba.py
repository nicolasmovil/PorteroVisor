
import RPi.GPIO as GPIO
import os
import subprocess


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(4)
    if input_state == False:
#        os.system('./prueba1expect.sh')

# Ejecuta el script de Expect
subprocess.call(["expect", "./prueba1expect.sh"])

# Espera 20 segundos
time.sleep(20)

# Cierra la aplicación
subprocess.call(["pkill", "./prueba1expect.sh"])
