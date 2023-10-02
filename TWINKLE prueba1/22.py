import RPi.GPIO as GPIO
import subprocess
import time
import sys
import tty
import termios
import os

class TwinkleInterface:

    def __init__(self):
        self.cleanup_previous_twinkle()
        GPIO.setmode(GPIO.BCM)
        self.setup_gpio(4, self.call_101)
        self.setup_gpio(14, self.call_102)
        self.setup_gpio(15, self.call_103)
        self.start_twinkle()

    def cleanup_previous_twinkle(self):
        print("Limpieza previa de twinkle...")
        subprocess.run(["pkill", "-f", "twinkle-console"])
        os.system("fuser -k 5060/udp")
        print("Limpieza completada.")

    def setup_gpio(self, gpio, callback):
        print(f"Configurando GPIO {gpio}...")
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(gpio, GPIO.FALLING, callback=callback, bouncetime=200)
        print(f"GPIO {gpio} configurado.")

    def get_char(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def make_call(self, number):
        print(f"Haciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n".encode())
        self.twinkle_process.stdin.flush()

    def call_101(self, channel=None):
        self.make_call(101)

    def call_102(self, channel=None):
        self.make_call(102)

    def call_103(self, channel=None):
        self.make_call(103)

    def start_twinkle(self):
        print("Iniciando twinkle-console...")
        self.twinkle_process = subprocess.Popen(["twinkle-console"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("twinkle-console iniciado.")
        self.check_status_timer()

    def check_status_timer(self):
        while True:
            time.sleep(900)  # 15 minutes
            self.check_twinkle_status()

    def check_twinkle_status(self):
        print("Comprobando estado de twinkle-console...")
        output = subprocess.check_output(["ps", "-A"])
        if b"twinkle" not in output:
            self.restart_twinkle()

    def restart_twinkle(self):
        print("Reiniciando twinkle-console...")
        self.cleanup()
        self.cleanup_previous_twinkle()
        self.start_twinkle()

    def main_loop(self):
        print("Abriendo la aplicación twinkle-console...")
        try:
            while True:
                char = self.get_char()
                print(f"Carácter ingresado: {char}")
                if char == '4':
                    self.call_101()
                elif char == '5':
                    self.call_102()
                elif char == '6':
                    self.call_103()
                elif char == 'q':
                    self.cleanup()
                    break
        except KeyboardInterrupt:
            print("\nFinalizando programa...")
            self.cleanup()

    def cleanup(self):
        print("Cerrando la aplicación twinkle-console...")
        self.twinkle_process.stdin.write(b"quit\n")
        self.twinkle_process.stdin.flush()
        self.twinkle_process.wait()
        print("La aplicación twinkle-console ha sido cerrada.")
        GPIO.cleanup()

if __name__ == "__main__":
    os.system('clear')
    interface = TwinkleInterface()
    interface.main_loop()
