import os
import time

# Montar Google Drive
# drive.mount('/content/drive')  # Solo necesario en Colab

# Definir el directorio 
DIRUTH = '/content/drive/My Drive/' 

def list_arch(directory):
    try:
        files = os.listdir(directory)
        file_dates = []  # Aquí definimos correctamente la variable

        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                # Obtener la fecha de modificación
                modi_time = os.path.getmtime(file_path)
                file_dates.append((file, modi_time))

        # Ordenar archivos por fecha de modificación (más reciente primero)
        file_dates.sort(key=lambda x: x[1], reverse=True)

        print("Archivos en el directorio ordenados por fecha de subida:")
        for file, modi_time in file_dates:
            print(f"{file} - {time.ctime(modi_time)}")  

    except FileNotFoundError:
        print("Directorio no encontrado.")
    except PermissionError:
        print("No tienes permiso para acceder a este directorio.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llamar a la función
list_arch(DIRUTH)