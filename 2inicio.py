import RPi.GPIO as GPIO
import keyboard
import time
import subprocess

# Desactivar la interfaz wlan0
subprocess.run(["sudo", "ifconfig", "wlan0", "down"])

# Esperar 5 segundos
time.sleep(10)

# Activar la interfaz wlan0
subprocess.run(["sudo", "ifconfig", "wlan0", "up"])

# AsignaciÃ³n de pines GPIO a botones
button_map = {
    7: "1",
    11: "2",
    9: "3",
    12: "A",
    22: "4",
    8: "5",
    25: "6",
    10: "B",
    4: "7",
    24: "8",
    23: "9",
    27: "C",
    15: "E",
    2: "0",
    14: "X",
    3: "D"
}

# ConfiguraciÃ³n de GPIO
GPIO.setmode(GPIO.BCM)
for pin, label in button_map.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Limpieza inicial de la pantalla
print("\033c", end="")

print("MODO ESPERA DE INGRESO DE BOTON")

# Bucle infinito para detectar pulsaciones del botÃ³n en cada GPIO y pulsaciones de teclado
try:
    while True:
        for pin, label in button_map.items():
            current_state = GPIO.input(pin)

            if current_state == GPIO.LOW and label in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "X", "E"]:
                print(f"DETECTADO BOTÃN {label} PRESIONADO")
                # Ejecutar llamar.py seguido del botÃ³n presionado (por ejemplo, "llamar.py 2" para el botÃ³n 2)
                subprocess.Popen(["python3", "/home/admin/fenixTecno/llamar.py", label])
                subprocess.Popen(["python3", "/home/admin/fenixTecno/llamadaluz.py"])
                time.sleep(5)

        if keyboard.is_pressed('1'):
            print("DETECTADA TECLA 1 PRESIONADA")
            # Ejecutar llamar.py seguido del botÃ³n presionado (por ejemplo, "llamar.py 1" para el botÃ³n 1)
            subprocess.Popen(["python3", "/home/admin/fenixTecno/llamar.py", "1"])
            subprocess.Popen(["python3", "/home/admin/fenixTecno/llamadaluz.py"])
            time.sleep(5)

        if keyboard.is_pressed('2'):
            print("DETECTADA TECLA 2 PRESIONADA")
            # Ejecutar llamar.py seguido del botÃ³n presionado (por ejemplo, "llamar.py 2" para el botÃ³n 2)
            subprocess.Popen(["python3", "/home/admin/fenixTecno/llamar.py", "2"])
            subprocess.Popen(["python3", "/home/admin/fenixTecno/llamadaluz.py"])
            time.sleep(5)

        time.sleep(0.1)

# Manejar Ctrl+C para salir limpiamente
except KeyboardInterrupt:
    pass

# Limpiar y configurar los pines GPIO antes de salir del programa
GPIO.cleanup()
