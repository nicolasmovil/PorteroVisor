import RPi.GPIO as GPIO
import subprocess
import time
import os

class TwinkleInterface:

    def __init__(self):
        os.system('clear')  # Limpia la pantalla
        self.kill_running_processes()
        self.setup_gpio()
        self.twinkle_process = subprocess.Popen(["twinkle-console"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def kill_running_processes(self):
        # Mata el proceso de twinkle-console
        subprocess.run(["pkill", "-9", "twinkle-console"])

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        self.gpio_map = {
            4: 111, 27: 121, 22: 131, 10: 141, 9: 151,
            11: 161, 5: 171, 6: 181, 13: 191, 19: 460833,
            26: 0, 14: 0, 15: 0, 23: 0, 24: 0, 25: 0, 8: 0, 7: 0, 12: 0, 16: 0, 20: 0, 21: 0
        }
        for gpio in self.gpio_map.keys():
            GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(gpio, GPIO.FALLING, callback=self.handle_gpio_event, bouncetime=200)

    def handle_gpio_event(self, channel):
        self.make_call(str(self.gpio_map[channel]))

    def make_call(self, number):
        print(f"Haciendo una llamada al número {number}...")
        self.twinkle_process.stdin.write(f"call {number}\n".encode())
        self.twinkle_process.stdin.flush()

        time.sleep(5)

        while True:
            output = self.twinkle_process.stdout.readline().decode("utf-8")
            print(output.strip())  # Muestra la salida de twinkle-console
            if "Line 1: call failed" in output:
                print("La llamada ha fallado. Volviendo a escuchar en GPIO y teclado...")
                break
            elif "Line 1: far end answered call." in output:
                print("La llamada ha sido contestada. Esperando 30 segundos antes de finalizar...")
                time.sleep(30)
                self.twinkle_process.stdin.write(b"--cmd bye\n")
                self.twinkle_process.stdin.flush()
                break
            elif "Line 1: far end ended call." in output:
                print("La llamada ha terminado. Volviendo a escuchar en GPIO y teclado...")
                break

    def main_loop(self):
        print("Abriendo la aplicación twinkle-console...")
        print("Posibles opciones de GPIO y números a los que se llamará:")
        for gpio, number in self.gpio_map.items():
            print(f"{gpio}: {number}")

        try:
            while True:
                input_data = input(f"Introduce el número de GPIO ({','.join(map(str, self.gpio_map.keys()))}) para emular o 'q' para salir: ")
                if input_data in map(str, self.gpio_map.keys()):
                    self.handle_gpio_event(int(input_data))
                elif input_data == 'q':
                    print("Comando 'quit' detectado. Finalizando...")
                    self.twinkle_process.stdin.write(b"quit\n")
                    self.twinkle_process.stdin.flush()
                    time.sleep(1)  # Damos tiempo para que el proceso se cierre adecuadamente
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
    interface = TwinkleInterface()
    interface.main_loop()
