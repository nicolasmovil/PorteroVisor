import RPi.GPIO as GPIO  # Importa el módulo RPi.GPIO para controlar el GPIO
import subprocess  # Importa el módulo subprocess para ejecutar comandos en la terminal
import time  # Importa el módulo time para pausar la ejecución del programa

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)  # Configura el modo del GPIO
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura el GPIO 4 como entrada con resistencia pull-up interna

# Agrega la detección de flanco al GPIO 4
GPIO.add_event_detect(4, GPIO.FALLING, callback=lambda _: None, bouncetime=200)

# Abre la aplicación twinkle-console utilizando Expect y redirige la salida a un archivo de registro
print("Abriendo la aplicación twinkle-console...")
with open("twinkle.log", "w") as log_file:
    twinkle = subprocess.Popen(["twinkle-console"], stdin=subprocess.PIPE, stdout=log_file, stderr=subprocess.STDOUT)

# Bucle principal
while True:  # Inicia un bucle infinito
    time.sleep(0.1)  # Espera 0.1 segundos para evitar un uso excesivo de la CPU

    if GPIO.event_detected(4):  # Verifica si se ha detectado un flanco de bajada en el GPIO 4
        print("Se ha detectado un flanco de bajada en el GPIO 4.")

        # Envía el comando para hacer una llamada al número 101
        print("Haciendo una llamada al número 101...")
        twinkle.stdin.write(b"call 101\n")
        twinkle.stdin.flush()

        # Espera 5 segundos para verificar si la llamada se ha realizado correctamente
        time.sleep(5)

        # Verifica si la llamada ha fallado
        with open("twinkle.log", "r") as log_file:
            output = log_file.read()
        if "Line 1: call failed" in output:
            print("La llamada ha fallado. Cancelando la espera de 30 segundos...")
            continue

        # Espera 30 segundos antes de enviar el comando "bye"
        print("La llamada se ha realizado correctamente. Esperando 30 segundos antes de finalizar la llamada...")
        time.sleep(30)

        # Envía el comando para finalizar la llamada
        print("Finalizando la llamada...")
        twinkle.stdin.write(b"--cmd bye\n")
        twinkle.stdin.flush()

        # Espera 1 segundo para evitar rebotes del botón
        time.sleep(1)

# Mata la aplicación twinkle-console
print("Cerrando la aplicación twinkle-console...")
twinkle.kill()
print("La aplicación twinkle-console ha sido cerrada.")
