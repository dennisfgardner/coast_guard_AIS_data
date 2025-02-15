import unittest

from marine_cadastre.config import Config
from marine_cadastre.utilities import list_files_by_type


class TestUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.config.data_dir = "./tests/data"

    def test_list_files_by_type(self):
        data_dir = self.config.data_dir
        file_names = list_files_by_type(data_dir, ".csv")
        ext = file_names[0].split(".")[-1]
        self.assertEqual(ext, "csv")
        self.assertEqual(len(file_names), 3)
        self.assertIn("AIS_test_00.csv", file_names)
        self.assertIn("AIS_test_01.csv", file_names)
        self.assertIn("AIS_test_02.csv", file_names)


if __name__ == '__main__':
    unittest.main()
