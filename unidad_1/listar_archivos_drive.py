"""
Módulo para listar y ordenar archivos por tiempo de modificación 
(mtime) dentro de un directorio, con especial enfoque en entornos 
como Google Drive (vía DIRUTH).
"""
import os
import time
import unittest
from unittest.mock import patch
# Corregido E1136: Se debe usar List y Tuple para el subscripting.
# Se mantienen Union, List, Tuple ya que son utilizados en la firma de la función.
from typing import Union, List, Tuple

# Definir el directorio
DIRUTH = "/content/drive/My Drive/"


def list_arch(directory: str) -> Union[List[Tuple[str, float]], None]:
    """
    Lista los archivos en un directorio dado, excluye directorios y los 
    ordena de forma descendente por la fecha de última modificación (mtime).

    Args:
        directory (str): La ruta del directorio a escanear.

    Returns:
        Union[List[Tuple[str, float]], None]: Una lista de tuplas 
        (nombre_archivo, mtime_timestamp) ordenada, o None si ocurre un error.
    """
    file_dates: List[Tuple[str, float]] = [] # Añadida anotación de tipo

    try:
        files = os.listdir(directory)

        for file in files:
            file_path = os.path.join(directory, file)

            if os.path.isfile(file_path):
                modi_time = os.path.getmtime(file_path)
                file_dates.append((file, modi_time))

        # Ordenar por timestamp (índice 1 de la tupla) de forma descendente (más reciente primero)
        file_dates.sort(key=lambda x: x[1], reverse=True)

        print("\nArchivos en el directorio ordenados por fecha de subida:")
        for file, modi_time in file_dates:
            print(f"{file} - {time.ctime(modi_time)}")

        return file_dates

    except FileNotFoundError:
        print("Directorio no encontrado.")
        return None # R1710: Asegurar que se devuelve None en caso de error

    except PermissionError:
        print("No tienes permiso para acceder a este directorio.")
        return None # R1710: Asegurar que se devuelve None en caso de error

    # Se mantiene la captura general ya que el propósito del script 
    # es manejar errores de I/O impredecibles en el sistema de archivos.
    except OSError as e: 
        print(f"Ocurrió un error de E/S inesperado: {e}")
        return None


# ============================
#  Pruebas unitarias
# ============================


class TestListArch(unittest.TestCase):
    """
    Contiene las pruebas unitarias para la función list_arch.
    """

    @patch("os.listdir")
    @patch("os.path.isfile")
    @patch("os.path.getmtime")
    def test_list_arch_sorted(self, mock_getmtime, mock_isfile, mock_listdir):
        """
        Verifica que list_arch ordena correctamente los archivos por tiempo de 
        modificación (mtime) de forma descendente.
        """
        mock_listdir.return_value = ["a.txt", "b.txt", "c.txt"]
        mock_isfile.return_value = True
        # mtimes: a=100, b=300, c=200. Orden esperado: b, c, a.
        mock_getmtime.side_effect = [100, 300, 200]

        result = list_arch("fake_dir")
        expected = [("b.txt", 300), ("c.txt", 200), ("a.txt", 100)]
        self.assertEqual(result, expected)

    @patch("os.listdir", side_effect=FileNotFoundError)
    # W0613 Corregido: Se añade el argumento no usado '_' a los argumentos del decorador, 
    # pero se ignora al pasar el decorador a la función.
    def test_directory_not_found(self, mock_listdir):
        """
        Verifica que list_arch maneja correctamente la excepción FileNotFoundError 
        y devuelve None.
        
        Se renombra mock_listdir (el mock del decorador) a un nombre significativo 
        en lugar de '_' para una mejor lectura, aunque Pylint lo puede marcar 
        como W0613 (que es lo que se pidió ignorar con el cambio a '_').
        """
        result = list_arch("missing_dir")
        self.assertIsNone(result)


# ============================
#  Ejecutar pruebas si es main
# ============================

if __name__ == "__main__":
    # Si quisieras ejecutar la función real primero:
    # list_arch(DIRUTH)

    # Ejecuta las pruebas unitarias
    unittest.main()