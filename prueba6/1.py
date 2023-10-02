import subprocess
import time
import sys

# Ejecutar linphonec
p = subprocess.Popen(["linphonec", "-C"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Esperar 3 segundos
time.sleep(1)

# Mapeo de extensiones
extension_map = {
    "1": "2001",
    "2": "2002",
    "3": "2003",
    "4": "2004",
    "5": "2005",
    "6": "2006",
    "7": "2007",
    "8": "2008",
    "9": "2009",
    "0": "2010",
    "A": "2100",
    "B": "2200",
    "C": "2300",
    "D": "2400",
    "X": "2500",
    "E": "3000"
}

# Leer el atributo con el que se ejecutó la aplicación
if len(sys.argv) == 2:
    extension_key = sys.argv[1]
else:
    extension_key = "2"  # Valor por defecto

# Obtener la extensión correspondiente
extension = extension_map.get(extension_key, "2")

# Enviar comando "call"
print(f"Llamando a la extensión {extension}...")
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
#time.sleep(10)