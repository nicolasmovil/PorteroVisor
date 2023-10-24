import subprocess
import time
import sys

# Ejecutar linphonec
p = subprocess.Popen(["linphonec", "-C"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
subprocess.run(["aplay", "llamando.wav"])


# Esperar 3 segundos
time.sleep(1)

# Mapeo de extensiones
extension_map = {
    "1": "4001",    #
    "2": "4002",    #
    "3": "4003",    #
    "4": "4004",    # 
    "5": "4005",    # audio tu llamdado no puede completarse
    "6": "4006",    # audio tu llamdado no puede completarse
    "7": "4007",    # audio tu llamdado no puede completarse
    "8": "4008",    # audio tu llamdado no puede completarse
    "9": "4009",    # audio tu llamdado no puede completarse
    "0": "4010",    # no anda el boton
    "A": "2100",    # audio tu llamdado no puede completarse
    "B": "2200",    # audio tu llamdado no puede completarse
    "C": "2400",    # llamada a pc
    "D": "2400",    # todos 
    "X": "2500",    # audio tu llamdado no puede completarse
    "E": "3000"     # audio tu llamdado no puede completarse
} 

# Leer el atributo con el que se ejecutÃ³ la aplicaciÃ³n
if len(sys.argv) == 2:
    extension_key = sys.argv[1]
else:
    extension_key = "2"  # Valor por defecto

# Obtener la extensiÃ³n correspondiente
extension = extension_map.get(extension_key, "2")

# Enviar comando "call"
print(f"Llamando a la extensiÃ³n {extension}...")
p.stdin.write(f"call {extension} --early-media\n".encode())
p.stdin.flush()

# Leer la respuesta
output = p.stdout.readline()
call_ended = False
start_time = time.time()
while output:
    print(output.decode(), end="")
    if b"ended" in output or b"error" in output:
        # Terminar el programa
        subprocess.Popen(["pkill", "-9", "linphonec"])
        call_ended = True
        break
        
        
    elif b"conn..ected." in output:
        # Iniciar temporizador de 6 segundos
        time.sleep(20)
        p.stdin.write(f"terminate\n".encode())
        # Terminar el programa si no se ha terminado la llamada
        time.sleep(1)
        subprocess.Popen(["pkill", "-9", "linphonec"])
        break
        
        
    output = p.stdout.readline()

# Esperar 10 segundos antes de finalizar el programa
time.sleep(30)