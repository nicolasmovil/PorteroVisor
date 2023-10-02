import RPi.GPIO as GPIO
import subprocess
import threading
import time

class LinphoneInterface:
    def __init__(self):
        # Mapeo de botones GPIO a números de teléfono
        self.button_map = {
            2: "2001",    # departamento 1, botón "1"
            3: "2002",    # departamento 2, botón "2"
            4: "2003",    # departamento 3, botón "3"
            22: "6414",   # departamento 4, botón "4"
            14: "6415",   # departamento 5, botón "5"
            15: "6416",   # departamento 6, botón "6"
            24: "6417",   # departamento 7, botón "7"
            25: "6418",   # departamento 8, botón "8"
            8: "6419",    # departamento 9, botón "9"
            9: "6420",    # departamento 10, botón "0"
            27: "6421",   # departamento A, botón "A"
            23: "6422",   # departamento B, botón "B"
            12: "6423",   # departamento C, botón "C"
            7: "6424",    # departamento D, botón "D"
            11: "6425",   # departamento X, botón "X"
            10: "6425"    # departamento E, botón "E"
        }

        # Credenciales SIP
        self.sip_host = "192.168.0.200"
        self.sip_username = "1000"
        self.sip_password = "Nicolas01"

        # Iniciar Linphone
        self.start_linphone()

        # Configuración de GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.button_map.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        # Iniciar hilos para escuchar botones y el teclado
        self.button_thread = threading.Thread(target=self.listen_buttons)
        self.button_thread.start()

        self.keyboard_thread = threading.Thread(target=self.listen_keyboard)
        self.keyboard_thread.start()

    def start_linphone(self):
        try:
            # Verificar si Linphone ya está en ejecución
            subprocess.check_output(["pidof", "linphonec"])
        except subprocess.CalledProcessError:
            # Iniciar Linphone si no está en ejecución
            subprocess.Popen(["linphonecsh", "init"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def listen_buttons(self):
        try:
            while True:
                for pin, number in self.button_map.items():
                    if GPIO.input(pin) == GPIO.LOW:
                        self.make_call(number)
                        time.sleep(2)  # Espera 2 segundos antes de continuar
        except KeyboardInterrupt:
            pass

    def listen_keyboard(self):
        try:
            while True:
                option = input("Presiona 'q' para salir: ").strip().lower()
                if option == 'q':
                    self.cleanup()
                    break
        except KeyboardInterrupt:
            pass

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        with open("linphone_log.txt", "a") as log_file:
            subprocess.Popen(
                ["linphonecsh", "dial", f"sip:{number}@{self.sip_host}"],
                stdin=subprocess.PIPE,
                stdout=log_file,  # Redirigir la salida a un archivo de registro
                stderr=subprocess.STDOUT
            )

    def cleanup(self):
        print("Cerrando Linphone y limpiando GPIO...")
        GPIO.cleanup()
        subprocess.Popen(["linphonecsh", "exit"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.button_thread.join()
        self.keyboard_thread.join()

if __name__ == "__main__":
    interface = LinphoneInterface()
