import RPi.GPIO as GPIO
import time

# Asignación de pines GPIO a botones
button_map = {
    17: "1",
#    14: "2",
 #   23: "4",
 #   24: "5",
#    27: "7",
##    22: "8",
##    28: "E",
 ##   19: "0"
}

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

for pin in button_map.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Bucle infinito para detectar pulsaciones del botón en cada GPIO
while True:
    # Crear un diccionario para almacenar el estado de los botones
    button_states = {label: " " for label in button_map.values()}

    for pin, label in button_map.items():
        current_state = GPIO.input(pin)
        
        # Verificar si el botón está presionado
        if current_state == GPIO.HIGH:
            button_states[label] = label

    # Limpiar la pantalla
    print("\033c", end="")

    # Mostrar el diseño de los botones
    print(" [  1  ] [  2  ] [  3  ] [  A  ]")
    print(" [  4  ] [  5  ] [  6  ] [  B  ]")
    print(" [  7  ] [  8  ] [  9  ] [  C  ]")
    print(" [  E  ] [  0  ] [  X  ] [  D  ]")
    print(" ")
    print(" ----------------------------- ")
    print(" ")
    
    # Mostrar el estado de los botones
    print(f" [  {button_states['1']}  ] [  ] [     ] [     ]")
  #  print(f" [  {button_states['4']}  ] [  {button_states['5']}  ] [     ] [     ]")
 #   print(f" [  {button_states['7']}  ] [  {button_states['8']}  ] [     ] [     ]")
    print(f" [     ] [     ] [     ] [     ]")

    time.sleep(0.1)