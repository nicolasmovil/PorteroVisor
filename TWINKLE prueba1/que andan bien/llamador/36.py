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

    def check_button_press(self):
        for pin, number in self.button_map.items():
            current_state = GPIO.input(pin)
            
            if current_state == GPIO.LOW and self.previous_button_states[pin] == GPIO.HIGH:
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
        print("\nEsperando ingreso de teclado...")

    def read_output(self):
        for line in self.twinkle_process.stdout:
            print(line, end='')
            if "Line 1: far end answered call" in line:
                if hasattr(self, 'end_timer') and self.end_timer:
                    self.end_timer.cancel()
            elif "Line 1: far end ended call" in line:
                self.end_timer = threading.Timer(30, self.end_call)
                self.end_timer.start()

    def listen_keyboard(self):
        while True:
            option = input("Ingrese un número de teclado o 'q' para salir:123456789 ")
            if option == 'q':
                self.twinkle_process.stdin.write("bye\nquit\n")
                self.twinkle_process.stdin.flush()
                self.cleanup()
                break
            number = self.button_map.get(option, None)
            if number is not None:
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
