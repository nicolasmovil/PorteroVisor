import subprocess

class CallHandler:
    def __init__(self, twinkle_process):
        self.twinkle_process = twinkle_process

    def make_call(self, number):
        # Asume que para hacer una llamada, el comando es 'call [número]'
        call_command = f"call {number}\n"
        self.twinkle_process.stdin.write(call_command)
        self.twinkle_process.stdin.flush()

    def end_call(self):
        # Asume que para finalizar una llamada, el comando es 'bye'
        self.twinkle_process.stdin.write("bye\n")
        self.twinkle_process.stdin.flush()

    def mute_call(self):
        # Asume que para silenciar una llamada, el comando es 'mute'
        self.twinkle_process.stdin.write("mute\n")
        self.twinkle_process.stdin.flush()

    # Puedes agregar otros métodos relacionados con la gestión de llamadas si es necesario
