import RPi.GPIO as GPIO
import time
import subprocess

# Asignación de pines GPIO a botones
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

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
for pin, label in button_map.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Limpieza inicial de la pantalla
print("\033c", end="")

print("MODO ESPERA DE INGRESO DE BOTON")

# Bucle infinito para detectar pulsaciones del botón en cada GPIO
try:
    while True:
        for pin, label in button_map.items():
            current_state = GPIO.input(pin)

            if current_state == GPIO.LOW and label in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "X", "E"]:
                print(f"DETECTADO BOTÓN {label} PRESIONADO")
                # Ejecutar llamar.py seguido del botón presionado (por ejemplo, "llamar.py 2" para el botón 2)
                subprocess.Popen(["python3", "llamar.py", label])
                subprocess.Popen(["python3", "llamadaluz.py"])
                time.sleep(5)
 
        time.sleep(0.1)

# Manejar Ctrl+C para salir limpiamente
except KeyboardInterrupt:
    pass

# Limpiar y configurar los pines GPIO antes de salir del programa
GPIO.cleanup()