import RPi.GPIO as GPIO
import subprocess
import threading
import time

class TwinkleInterface:
    def __init__(self):
        # Botones y números asociados
        self.button_map = {
            15: "6411",
            14: "6412",
            23: None,  # No conectado
            24: "6414",
            27: "6415",
            22: "6416"
        }

        # Configura GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.button_map.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
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

    def check_button_press(self):
        for pin, number in self.button_map.items():
            current_state = GPIO.input(pin)
            if current_state == GPIO.HIGH and number is not None:
                self.make_call(number)

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n")
        self.twinkle_process.stdin.flush()
        timer = threading.Timer(30, self.end_call)
        timer.start()

    def end_call(self):
        print("\nTerminando la llamada después de 30 segundos...")
        self.twinkle_process.stdin.write("--cmd bye\n")
        self.twinkle_process.stdin.flush()

    def read_output(self):
        for line in self.twinkle_process.stdout:
            print(line, end='')

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
        self.thread.join()

if __name__ == "__main__":
    interface = TwinkleInterface()
    interface.main_loop()
