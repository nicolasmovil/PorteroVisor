import os
from github import Github

# Reemplaza con tus credenciales de autenticaciÃ³n de GitHub
usuario = "nicolasmovil"
contrasena = "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"
repositorio = "PorteroVisor"
ruta_carpeta = "/home/admin/fenixTecno"

# Crea una instancia de la clase Github con tus credenciales
g = Github(usuario, contrasena)

# Obtiene el repositorio
repo = g.get_user().get_repo(repositorio)

# Pide al usuario el mensaje del commit
mensaje_commit = input("Ingrese el mensaje del commit: ")

# Listar todos los archivos en la carpeta y subcarpetas
archivos = []
for dirpath, dirnames, filenames in os.walk(ruta_carpeta):
    for filename in filenames:
        archivo = os.path.join(dirpath, filename)
        archivos.append(archivo)

# Sube cada archivo al repositorio
for archivo in archivos:
    # Calcula la ruta relativa del archivo en la carpeta
    ruta_relativa = os.path.relpath(archivo, ruta_carpeta)

    # Verifica si el archivo ya existe en el repositorio
    try:
        contenido_archivo = repo.get_contents(ruta_relativa, ref="master")
    except Exception as e:
        contenido_archivo = None

    if contenido_archivo:
        # El archivo existe, obtÃ©n su "sha" para actualizarlo
        sha = contenido_archivo.sha

        # Lee el contenido del archivo con codificaciÃ³n Latin-1
        with open(archivo, 'r', encoding='latin-1') as file:
            contenido_archivo = file.read()

        # Actualiza el archivo en el repositorio
        repo.update_file(ruta_relativa, mensaje_commit, contenido_archivo, sha, branch="master")
    else:
        # El archivo no existe, crÃ©alo en el repositorio
        with open(archivo, 'r', encoding='latin-1') as file:
            contenido_archivo = file.read()

        # Crea el archivo en el repositorio
        repo.create_file(ruta_relativa, mensaje_commit, contenido_archivo, branch="master")
