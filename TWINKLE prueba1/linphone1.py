import RPi.GPIO as GPIO
import subprocess
import threading
import time
import os

class LinphoneInterface:
    def __init__(self, sip_host, sip_username, sip_password):
        os.system('clear')  # Limpiar pantalla al iniciar

        # Configuración de Linphone CLI
        self.sip_host = sip_host
        self.sip_username = sip_username
        self.sip_password = sip_password
        linphone_command = [
            "linphonecsh",
            "init",
            f"--host {self.sip_host}",
            f"--username {self.sip_username}",
            f"--password {self.sip_password}"
        ]
        self.linphone_process = subprocess.Popen(
            linphone_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Iniciar threads
        self.thread = threading.Thread(target=self.read_output)
        self.thread.start()


    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        command = f"call sip:{number}@{self.sip_host}"
        self.linphone_process.stdin.write(f"{command}\n")
        self.linphone_process.stdin.flush()

    def end_call(self):
        print("\nTerminando la llamada...")
        self.linphone_process.stdin.write("exit\n")
        self.linphone_process.stdin.flush()
        print("\nEsperando ingreso de teclado...")

    def read_output(self):
        linphone_command = [
            "linphonecsh",
            "init",
            f"--host {self.sip_host}",
            f"--username {self.sip_username}",
            f"--password {self.sip_password}"
        ]
        self.linphone_process = subprocess.Popen(
            linphone_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        for line in self.linphone_process.stdout:
            print(line, end='')
            if "Call terminated" in line:
                self.end_call()

    def main_loop(self):
        try:
            while True:
                option = input("Ingrese un número de teléfono o 'q' para salir: ").strip()
                if option == 'q':
                    self.end_call()
                    break
                if option.isdigit():
                    self.make_call(option)
        except KeyboardInterrupt:
            self.end_call()

if __name__ == "__main__":
    sip_host = "192.168.0.200"  # Cambia esto a la dirección de tu servidor SIP
    sip_username = "1000"       # Cambia esto a tu nombre de usuario SIP
    sip_password = "Nicolas01"  # Cambia esto a tu contraseña SIP

    interface = LinphoneInterface(sip_host, sip_username, sip_password)
    interface.main_loop()
