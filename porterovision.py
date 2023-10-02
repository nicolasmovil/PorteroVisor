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
for pin in button_map.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

history = []
max_history_length = 10

# Bucle infinito para detectar pulsaciones del botón en cada GPIO
while True:
    # Crear un diccionario para almacenar el estado de los botones
    button_states = {label: " " for label in button_map.values()}

    for pin, label in button_map.items():
        current_state = GPIO.input(pin)

        if current_state == GPIO.LOW and label not in button_states.values():
            button_states[label] = label
            history.append(label)
            if len(history) > max_history_length:
                history.pop(0)

            if label == "1":
                print("Botón 1 presionado")
                subprocess.run(["python3", "llamar.py"])  # Ejecutar llamar.py

    # Resto del código para mostrar el estado de los botones y el historial
    # ...

    time.sleep(0.1)
