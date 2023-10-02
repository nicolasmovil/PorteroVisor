import RPi.GPIO as GPIO
import time
import subprocess
import threading
from call_handler import CallHandler
from config import BUTTON_MAP

class TwinkleInterface:
    def __init__(self):
        # Ejecutar script bash y esperar 3 segundos
        subprocess.run(["bash", "matar.sh"])
        time.sleep(3)

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

        self.call_handler = CallHandler(self.twinkle_process)
        
        # Configuración de GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in BUTTON_MAP.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        
        self.previous_button_states = {pin: GPIO.HIGH for pin in BUTTON_MAP.keys()}
        
        self.listen_for_calls = True

        self.thread = threading.Thread(target=self.read_output)
        self.thread.start()

        self.keyboard_thread = threading.Thread(target=self.listen_keyboard)
        self.keyboard_thread.start()

    def check_button_press(self):
        for pin, mapping in BUTTON_MAP.items():
            if not self.listen_for_calls:
                break
            current_state = GPIO.input(pin)
            if current_state == GPIO.LOW and self.previous_button_states[pin] == GPIO.HIGH:
                number = mapping['call_number']
                self.call_handler.make_call(number)
            self.previous_button_states[pin] = current_state

    def read_output(self):
        for line in self.twinkle_process.stdout:
            print(line, end='')
            if any(keyword in line for keyword in ["Line 1: far end answered call", "Line 1: far end ended call", "Line 1: call failed"]):
                self.listen_for_calls = True
                print("\033[92mESPERANDO INGRESO\033[0m")  # Imprime en color verde

    def listen_keyboard(self):
        while True:
            option = input("Ingrese un número de teclado o 'q' para salir: ")
            if option == 'q':
                self.cleanup()
                break

            for pin, mapping in BUTTON_MAP.items():
                if mapping['keyboard'] == option:
                    number = mapping['call_number']
                    self.call_handler.make_call(number)
                    break

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
        self.twinkle_process.terminate()
        self.thread.join()

if __name__ == "__main__":
    interface = TwinkleInterface()
    interface.main_loop()
