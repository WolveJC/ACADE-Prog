import os
import time
import unittest
from unittest.mock import patch

# Definir el directorio
DIRUTH = "/content/drive/My Drive/"


def list_arch(directory):
    try:
        files = os.listdir(directory)
        file_dates = []

        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                modi_time = os.path.getmtime(file_path)
                file_dates.append((file, modi_time))

        file_dates.sort(key=lambda x: x[1], reverse=True)

        print("Archivos en el directorio ordenados por fecha de subida:")
        for file, modi_time in file_dates:
            print(f"{file} - {time.ctime(modi_time)}")

        return file_dates  # útil para pruebas

    except FileNotFoundError:
        print("Directorio no encontrado.")
    except PermissionError:
        print("No tienes permiso para acceder a este directorio.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


# ============================
#  Pruebas unitarias
# ============================


class TestListArch(unittest.TestCase):

    @patch("os.listdir")
    @patch("os.path.isfile")
    @patch("os.path.getmtime")
    def test_list_arch_sorted(self, mock_getmtime, mock_isfile, mock_listdir):
        mock_listdir.return_value = ["a.txt", "b.txt", "c.txt"]
        mock_isfile.return_value = True
        mock_getmtime.side_effect = [100, 300, 200]

        result = list_arch("fake_dir")
        expected = [("b.txt", 300), ("c.txt", 200), ("a.txt", 100)]
        self.assertEqual(result, expected)

    @patch("os.listdir", side_effect=FileNotFoundError)
    def test_directory_not_found(self, mock_listdir):
        result = list_arch("missing_dir")
        self.assertIsNone(result)


# ============================
#  Ejecutar pruebas si es main
# ============================

if __name__ == "__main__":
    unittest.main()
