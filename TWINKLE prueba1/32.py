import RPi.GPIO as GPIO
import subprocess
import threading
import os

class TwinkleInterface:
    def __init__(self):
        # Limpia la pantalla
        os.system('clear')

        # Mata el proceso de twinkle-console
        os.system('pkill -9 twinkle-console')

        # Define los números asociados a cada GPIO
        self.gpio_map = {
            '01': (4, '6411'),
            '02': (27, '6412'),
            '03': (22, '6413'),
            '04': (10, '6414'),
            '05': (9, '6415'),
            '06': (11, '6416'),
            '07': (5, '6417'),
            '08': (6, '6418'),
            '09': (13, '6419'),
            '10': (19, '2001')
        }

        # Configura los GPIO
        self.setup_gpio()

        # Abre el proceso de twinkle-console
        self.twinkle_process = subprocess.Popen(["twinkle-console"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for _, (gpio, _) in self.gpio_map.items():
            GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(gpio, GPIO.FALLING, callback=self.handle_gpio_event, bouncetime=200)

    def handle_gpio_event(self, channel):
        for dept, (gpio, number) in self.gpio_map.items():
            if gpio == channel:
                self.make_call(number)

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n".encode())
        self.twinkle_process.stdin.flush()

        timer = threading.Timer(30, self.end_call)
        timer.start()

    def end_call(self):
        print("\nTerminando la llamada después de 30 segundos...")
        self.twinkle_process.stdin.write(b"--cmd bye\n")
        self.twinkle_process.stdin.flush()

    def main_loop(self):
        try:
            while True:
                print("\nOpciones disponibles:")
                for dept, (gpio, number) in self.gpio_map.items():
                    print(f"Departamento {dept} - GPIO {gpio} - Número {number}")
                input_data = input("\nIntroduce el número de departamento para llamar, o 'q' para salir: ")
                if input_data in self.gpio_map.keys():
                    _, number = self.gpio_map[input_data]
                    self.make_call(number)
                elif input_data == 'q':
                    print("Comando 'quit' detectado. Finalizando...")
                    self.twinkle_process.stdin.write(b"quit\n")
                    self.twinkle_process.stdin.flush()
                    break
                else:
                    print("Entrada inválida.")
        except KeyboardInterrupt:
            print("\nFinalizando programa...")
        finally:
            self.cleanup()

    def cleanup(self):
        print("Cerrando la aplicación twinkle-console...")
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        interface = TwinkleInterface()
        interface.main_loop()
    except AttributeError as e:
        print(f"Error: {e}. Probablemente hay un problema con la definición de la clase o la llamada a uno de sus métodos.")
