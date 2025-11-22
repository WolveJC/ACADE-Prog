import unittest
from unittest.mock import patch
from listar_archivos import list_arch

class TestListArch(unittest.TestCase):
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    def test_list_arch_sorted(self, mock_getmtime, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['a.txt', 'b.txt', 'c.txt']
        mock_isfile.return_value = True
        mock_getmtime.side_effect = [100, 300, 200]

        result = list_arch('fake_dir')
        expected = [('b.txt', 300), ('c.txt', 200), ('a.txt', 100)]
        self.assertEqual(result, expected)