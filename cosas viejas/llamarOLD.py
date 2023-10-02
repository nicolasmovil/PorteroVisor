import subprocess
import threading
import time
import os
import sys

class LinphoneInterface:
    def __init__(self):
        os.system('clear')  # Limpiar pantalla al iniciar

        # Mapeo de teclado a número de extensión SIP
        self.keyboard_map = {
            "1": "2001",
            "2": "2002",
            "3": "2003",
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

        # Iniciar Linphonec
        self.linphone_process = subprocess.Popen(
            ["linphonecsh", "init"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        self.thread = threading.Thread(target=self.read_output)
        self.thread.start()

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.linphone_process.stdin.write(f"call {number}\n")
        self.linphone_process.stdin.flush()

    def end_call(self):
        print("\nTerminando la llamada...")
        self.linphone_process.stdin.write("terminate all\n")
        self.linphone_process.stdin.flush()

    def unregister(self):
        print("\nDesregistrando Linphonec...")
        self.linphone_process.stdin.write("unregister\n")
        self.linphone_process.stdin.flush()

    def read_output(self):
        for line in self.linphone_process.stdout:
            print(line, end='')
            if "Call with destination" in line and "is terminated" in line:
                self.cleanup()  # Llama a la función cleanup cuando se detecta el fin de la llamada

            if "Call to" in line and "failed" in line:
                print("Error en la llamada.")
                self.cleanup()  # Llama a la función cleanup cuando se produce un error en la llamada

            if "Ready" in line:
                print("Linphonec está listo para hacer llamadas.")
                time.sleep(2)  # Esperar 2 segundos para que Linphonec se registre antes de hacer la llamada

            if "Registering to" in line:
                print("Registrándose en el servidor SIP...")

            if "Registration successful" in line:
                print("Registración exitosa.")

    def cleanup(self):
        print("Cerrando la aplicación Linphonec...")
        self.end_call()  # Terminar todas las llamadas antes de salir
        self.unregister()  # Desregistrarse antes de salir
        self.linphone_process.stdin.write("quit\n")
        self.linphone_process.stdin.flush()
        self.linphone_process.wait()  # Esperar a que Linphonec se cierre completamente

if __name__ == "__main__":
    interface = LinphoneInterface()
    if len(sys.argv) > 1:
        department = sys.argv[1]
        number = interface.keyboard_map.get(department, None)
        if number is not None:
            interface.make_call(number)
            interface.thread.join()  # Esperar a que termine el hilo de Linphone
        else:
            print(f"No se encontró el número de extensión SIP para el departamento {department}.")
            sys.exit(1)  # Salir con código de error
    else:
        print("Debe proporcionar un número de departamento como argumento.")
        sys.exit(1)  # Salir con código de error
