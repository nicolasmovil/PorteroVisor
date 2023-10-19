import subprocess
import time
import os
 
# Verificar si se estÃ¡ ejecutando como administrador
if os.geteuid() != 0:
    print("Este script debe ejecutarse con privilegios de administrador (sudo).")
    exit(1)

# Reproducir el sonido "whatchdog.wav" al inicio
subprocess.run(["aplay", "whatchdog.wav"])
 
# ParÃ¡metros
max_retries = 5
retry_interval = 10
ping_target = "8.8.8.8"
wifi_interface = "wlan0"
zerotier_network = "41d49af6c2981a7e"

# Variable para controlar la visualizaciÃ³n de la salida en la terminal
ver_salida_terminal = False

# FunciÃ³n para reiniciar la interfaz WiFi
def restart_wifi():
    subprocess.run(["aplay", "reiniciandowifi.wav"])
    subprocess.run(["sudo", "ifconfig", wifi_interface, "down"])
    time.sleep(10)
    subprocess.run(["sudo", "ifconfig", wifi_interface, "up"])

# Esperar 20 segundos antes de reiniciar el WiFi
time.sleep(8)
restart_wifi()

while True:  # Bucle infinito
    retry_count = 0
    connected = False  # Variable para controlar el estado de la conexiÃ³n

    while retry_count < max_retries:
        ping_process = subprocess.Popen(["ping", "-c", "1", ping_target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_output, ping_error = ping_process.communicate()

        if ping_process.returncode == 0:
            if not connected:
                subprocess.run(["aplay", "conexion.wav"])  # Reproducir solo cuando se restablece la conexiÃ³n
                connected = True
            retry_count = 0  # Reiniciar contador de intentos fallidos
        else:
            retry_count += 1
            if retry_count >= max_retries:
                connected = False  # La conexiÃ³n se pierde
                restart_wifi()
                zerotier_process = subprocess.Popen(["zerotier-cli", "join", zerotier_network], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                zerotier_output, zerotier_error = zerotier_process.communicate()
                subprocess.run(["aplay", "sinconexion.wav"])

        if ver_salida_terminal:
            print("Salida de ping:")
            print(ping_output.decode('utf-8'))
            print("Error de ping:")
            print(ping_error.decode('utf-8'))

        time.sleep(retry_interval)
reboot