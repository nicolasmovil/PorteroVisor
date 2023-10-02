import RPi.GPIO as GPIO
import subprocess
import threading
import time
import os

class TwinkleInterface:
    def __init__(self):
        os.system('clear')  # Limpiar pantalla al iniciar
        os.system('bash matar.sh')  # Ejecutar el script bash matar.sh
        time.sleep(3)  # Espera 3 segundos antes de continuar

        self.is_listening = True  # Variable para controlar si escucha los GPIOs

        # Asignación de pines GPIO a botones y números de teclado
        self.button_map = {
            2: "6411",    # departamento 1, botón "1"
            3: "6412",    # departamento 2, botón "2"
            4: "6413",    # departamento 3, botón "3"
            22: "6414",   # departamento 4, botón "4"
            27: "6415",   # departamento 5, botón "5"
            10: "6416",   # departamento 6, botón "6"
            11: "6417",   # departamento 7, botón "7"
            5: "6418",    # departamento 8, botón "8"
            6: "6419",    # departamento 9, botón "9"
            26: "6420",   # departamento 10, botón "0"
            17: "6421",   # departamento A, botón "A"
            9: "6422",    # departamento B, botón "B"
            13: "6423",   # departamento C, botón "C"
            14: "6424",   # departamento D, botón "D"
            15: "6425"    # departamento X, botón "X"
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

        print("\033[94m\033[1mESPERANDO INGRESO\033[0m")  # Mensaje en azul y en negrita

    def check_button_press(self):
        if not self.is_listening:  # Si no está escuchando, no hace nada
            return

        for pin, number in self.button_map.items():
            current_state = GPIO.input(pin)
            
            if current_state == GPIO.LOW and self.previous_button_states[pin] == GPIO.HIGH:
                self.is_listening = False  # Deja de escuchar una vez detectado un botón
                self.make_call(number)
            
            self.previous_button_states[pin] = current_state

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n")
        self.twinkle_process.stdin.flush()

    def end_call(self):
        print("\nTerminando la llamada...")
        self.twinkle_process.stdin.write("bye\n")
        self.twinkle_process.stdin.flush()
        self.is_listening = True  # Reanuda la escucha de los GPIOs al terminar la llamada
        print("\033[94m\033[1mESPERANDO INGRESO\033[0m")  # Mensaje en azul y en negrita

    def read_output(self):
        for line in self.twinkle_process.stdout:
            print(line, end='')
            if "Line 1: far end ended call" in line or "Line 1: call failed." in line:
                self.end_call()

    def listen_keyboard(self):
        while True:
            option = input("Ingrese un número de teclado o 'q' para salir: ")
            if option == 'q':
                self.cleanup()
                break
            if not option.isdigit():
                print("Entrada no válida. Intente nuevamente.")
                continue
            # Aquí, en lugar de buscar en `self.button_map` directamente, primero convertimos la opción en una clave.
            key = list(self.button_map.keys())[int(option) - 1]
            number = self.button_map.get(key, None)
            if number is not None:
                self.is_listening = False
                self.make_call(number)

    def main_loop(self):
        try:
            while True:
                self.check_button_press()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        if hasattr(self, 'is_cleaned_up') and self.is_cleaned_up:
            return

        print("Cerrando la aplicación twinkle-console...")
        GPIO.cleanup()
        self.twinkle_process.stdin.write("quit\n")
        self.twinkle_process.stdin.flush()
        self.twinkle_process.terminate()  # Asegurarse de que el subproceso termine correctamente
        self.thread.join()

        if threading.current_thread() != self.keyboard_thread:
            self.keyboard_thread.join()

        self.is_cleaned_up = True

if __name__ == "__main__":
    interface = TwinkleInterface()
    interface.main_loop()
