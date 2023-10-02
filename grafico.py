import RPi.GPIO as GPIO
import time
#--------------------------------------
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



#button_map = {
#     2: "1",
#     3: "2",
#     4: "3",
#    17: "A",
#    22: "4",
#    27: "5",
#    10: "6",
#     9: "B",
#    11: "7",
#     5: "8",
#     6: "9",
#    13: "C",
#    19: "E",
#    26: "0",
#    15: "X",
#    14: "D"


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
    print(f" [  {button_states['1']}  ] [  {button_states['2']}  ] [  {button_states['3']}  ] [  {button_states['A']}  ]")
    print(f" [  {button_states['4']}  ] [  {button_states['5']}  ] [  {button_states['6']}  ] [  {button_states['B']}  ]")
    print(f" [  {button_states['7']}  ] [  {button_states['8']}  ] [  {button_states['9']}  ] [  {button_states['C']}  ]")
    print(f" [  {button_states['E']}  ] [  {button_states['0']}  ] [  {button_states['X']}  ] [  {button_states['D']}  ]")
    print(" ")
    print("Historial de botones presionados:")
    print(", ".join(history))

    time.sleep(0.1)
