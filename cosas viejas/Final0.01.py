import RPi.GPIO as GPIO
import subprocess
import threading
import time
import os

class TwinkleInterface:
    def __init__(self):
        os.system('clear')  # Limpiar pantalla al iniciar

        # Asignación de pines GPIO a botones
        self.button_map = {
            7: "2001",    # departamento 1, botón "1" 
            11: "2002",    # departamento 2, botón "2"
            9: "2003",    # departamento 3, botón "3"
            22: "6414",   # departamento 4, botón "4"
            8: "6415",   # departamento 5, botón "5"
            25: "6416",   # departamento 6, botón "6"
            4: "6417",   # departamento 7, botón "7"
            24: "6418",   # departamento 8, botón "8"
            23: "6419",   # departamento 9, botón "9"
            2: "6420",   # departamento 10, botón "0"
            12: "6421",   # departamento A, botón "A"
            10: "6422",   # departamento B, botón "B"
            27: "6423",   # departamento C, botón "C"
            3: "6424",   # departamento D, botón "D"
            14: "6425",   # departamento X, botón "X"
            15: "6425"    # departamento E, botón "E"
        }

        # Mapeo de teclado a número
        self.keyboard_map = {
            "1": "6411",
            "2": "6412",
            "3": "6413",
            "4": "6414",
            "5": "6415",
            "6": "6416",
            "7": "6417",
            "8": "6418",
            "9": "6419",
            "0": "6420",
            "A": "6421",
            "B": "6422",
            "C": "6423",
            "D": "6424",
            "X": "6425",
            "E": "6425"
        }

        # Configuración de GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.button_map.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)    
        self.previous_button_states = {pin: GPIO.HIGH for pin in self.button_map.keys()}
        
        # Iniciar twinkle-console
        self.twinkle_process = subprocess.Popen(
            ["twinkle-console"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        self.thread = threading.Thread(target=self.read_output)
        self.thread.start()

        self.keyboard_thread = threading.Thread(target=self.listen_keyboard)
        self.keyboard_thread.start()

    def check_button_press(self):
        for pin, number in self.button_map.items():
            current_state = GPIO.input(pin)
            
            if current_state == GPIO.LOW and self.previous_button_states[pin] == GPIO.HIGH:
                self.turn_off_camera()  # Apagar la cámara antes de la llamada
                self.make_call(number)
            
            self.previous_button_states[pin] = current_state

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n")
        self.twinkle_process.stdin.flush()

    def turn_off_camera(self):
        print("\nApagando la cámara...")
        self.twinkle_process.stdin.write("camera off\n")
        self.twinkle_process.stdin.flush()
        print("Cámara apagada.")

    def end_call(self):
        print("\nTerminando la llamada...")
        self.twinkle_process.stdin.write("bye\n")
        self.twinkle_process.stdin.flush()
        self.twinkle_process.wait()  # Esperar a que Linphone se cierre
        
    def read_output(self):
        for line in self.twinkle_process.stdout:
            print(line, end='')
            if "Call 1 with sip:" in line and "ended" in line:
                self.end_call()
                self.cleanup()
                break

    def listen_keyboard(self):
        while True:
            option = input("Ingrese un número de teclado o 'q' para salir:123456789 ").upper()  # Convertimos la entrada a mayúscula
            if option == 'Q':
                self.twinkle_process.stdin.write("bye\nquit\n")
                self.twinkle_process.stdin.flush()
                self.cleanup()
                break
            number = self.keyboard_map.get(option, None)  # Usamos keyboard_map en lugar de button_map
            if number is not None:
                self.turn_off_camera()  # Apagar la cámara antes de la llamada
                self.make_call(number)

    def main_loop(self):
        try:
            while True:
                self.check_button_press()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        print("Cerrando la aplicación twinkle-console...")
        GPIO.cleanup()
        self.twinkle_process.stdin.write("quit\n")
        self.twinkle_process.stdin.flush()
        self.twinkle_process.terminate()  # Asegurarse de que el subproceso termine correctamente
        self.thread.join()
        self.keyboard_thread.join()

if __name__ == "__main__":
    interface = TwinkleInterface()
    interface.main_loop()
