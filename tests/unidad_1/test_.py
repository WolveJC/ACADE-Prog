"""
Módulo de pruebas unitarias para la función list_arch del módulo
unidad_1/listar_archivos_drive.py.

Utiliza unittest.mock para simular las llamadas al sistema de archivos 
(os.listdir, os.path.isfile, os.path.getmtime) y garantizar que la función
list_arch ordena correctamente los archivos por tiempo de modificación.
"""
import unittest
from unittest.mock import patch
# Se asume que la estructura de tu proyecto es correcta para esta importación
from unidad_1.listar_archivos_drive import list_arch


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
        modificación (mtime) de forma descendente (el más reciente primero).
        
        Mocks:
        - mock_listdir: Simula la lista de archivos en el directorio.
        - mock_isfile: Simula que todos los elementos son archivos.
        - mock_getmtime: Simula los tiempos de modificación (timestamps).
        """
        # Configuramos los valores simulados
        mock_listdir.return_value = ["a.txt", "b.txt", "c.txt"]
        mock_isfile.return_value = True
        # Asignamos mtimes a [a.txt, b.txt, c.txt] -> [100, 300, 200]
        mock_getmtime.side_effect = [100, 300, 200]

        # Ejecución de la función bajo prueba
        result = list_arch("fake_dir")
        
        # El orden esperado debe ser el más reciente primero (300, 200, 100)
        expected = [("b.txt", 300), ("c.txt", 200), ("a.txt", 100)]
        
        # Aserción
        self.assertEqual(result, expected)