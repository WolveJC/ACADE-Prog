import os
import time
from google.colab import drive

# Montar Google Drive
drive.mount('/content/drive')

# Directorio base (ajusta si tu Drive usa "My Drive" en vez de "MyDrive")
DIRUTH = '/content/drive/MyDrive/'

def format_size(size_bytes):
    """Convierte el tamaño en bytes a la unidad más adecuada."""
    if size_bytes == 0:
        return "0 Bytes"
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    # Mostrar sin decimales si es entero, con 2 decimales si no
    if size_bytes.is_integer():
        return f"{int(size_bytes)} {units[i]}"
    else:
        return f"{size_bytes:.2f} {units[i]}"

def list_arch(directory):
    try:
        files = os.listdir(directory)
        items = []

        for file in files:
            file_path = os.path.join(directory, file)
            modi_time = os.path.getmtime(file_path)

            if os.path.isdir(file_path):
                items.append((file, modi_time, "Carpeta", None))  # tamaño no aplica
            elif os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                items.append((file, modi_time, "Archivo", size))

        # Ordenar: primero carpetas, luego archivos, ambos por fecha descendente
        items.sort(key=lambda x: (x[2] != "Carpeta", -x[1]))

        print("Contenido del directorio ordenado (carpetas primero):\n")
        for file, modi_time, tipo, size in items:
            fecha = time.ctime(modi_time)
            if tipo == "Archivo":
                print(f"{file} | {tipo} | {format_size(size)} | {fecha}")
            else:
                print(f"{file} | {tipo} | -- | {fecha}")

    except FileNotFoundError:
        print("Directorio no encontrado.")
    except PermissionError:
        print("No tienes permiso para acceder a este directorio.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llamar a la función
list_arch(DIRUTH)