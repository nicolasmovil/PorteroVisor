import subprocess
import threading
import time
import os

class LinphoneInterface:
    def __init__(self):
        os.system('clear')  # Limpiar pantalla al iniciar

        # Asignación de pines GPIO a botones
        self.button_map = {
            7: "2001",    # departamento 1, botón "1" 
            11: "2002",    # departamento 2, botón "2"
            9: "2003",    # departamento 3, botón "3"
            22: "6414",   # departamento 4, botón "4"
            8: "6415",   # departamento 5, botón "5"
            25: "6416",   # departamento 6, botón "6"
            4: "6417",   # departamento 7, botón "7"
            24: "6418",   # departamento 8, botón "8"
            23: "6419",   # departamento 9, botón "9"
            2: "6420",   # departamento 10, botón "0"
            12: "6421",   # departamento A, botón "A"
            10: "6422",   # departamento B, botón "B"
            27: "6423",   # departamento C, botón "C"
            3: "6424",   # departamento D, botón "D"
            14: "6425",   # departamento X, botón "X"
            15: "6425"    # departamento E, botón "E"
        }

        # Mapeo de teclado a número
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
            ["linphonec", "-C"],
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

    def make_call(self, number):
        print(f"\nHaciendo una llamada al número {number}...")
        self.linphone_process.stdin.write(f"call sip:{number}@192.168.0.200 --early-media\n")
        self.linphone_process.stdin.flush()

    def end_call(self):
        print("\nTerminando la llamada...")
        self.linphone_process.stdin.write("bye\nquit\n")
        self.linphone_process.stdin.flush()
        print("\nEsperando ingreso de teclado...")

    def read_output(self):
        for line in self.linphone_process.stdout:
            print(line, end='')
            if "Call with sip:" in line and "early media." in line:
                if hasattr(self, 'end_timer') and self.end_timer:
                    self.end_timer.cancel()
            elif "Call with sip:" in line and "connected." in line:
                self.end_timer = threading.Timer(30, self.end_call)
                self.end_timer.start()

    def listen_keyboard(self):
        while True:
            option = input("Ingrese un número de teclado o 'q' para salir: ").upper()  # Convertimos la entrada a mayúscula
            if option == 'Q':
                self.cleanup()
                break
            number = self.keyboard_map.get(option, None)  # Usamos keyboard_map en lugar de button_map
            if number is not None:
                self.make_call(number)

    def cleanup(self):
        print("Cerrando la aplicación Linphonec...")
        self.linphone_process.terminate()  # Asegurarse de que el subproceso termine correctamente

if __name__ == "__main__":
    interface = LinphoneInterface()
    interface.make_call("2002")  # Puedes establecer la llamada inicial aquí si lo deseas
    interface.listen_keyboard()  # Esperar a que el usuario realice más llamadas desde el teclado
