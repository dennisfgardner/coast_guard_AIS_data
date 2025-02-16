import unittest

from marine_cadastre.config import Config
import marine_cadastre.utilities as ut


class TestUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.config.data_dir = "./tests/data"

    def test_list_files_by_type(self):
        file_names = ut.list_files_by_type(self.config.data_dir, ".csv")
        ext = file_names[0].split(".")[-1]
        self.assertEqual(ext, "csv")
        self.assertEqual(len(file_names), 3)
        self.assertIn("AIS_test_00.csv", file_names)
        self.assertIn("AIS_test_01.csv", file_names)
        self.assertIn("AIS_test_02.csv", file_names)

    def test_is_mmsi_vessel(self):
        self.assertTrue(ut.is_mmsi_vessel(200000000))
        self.assertTrue(ut.is_mmsi_vessel(338126914))
        self.assertTrue(ut.is_mmsi_vessel(799999999))
        self.assertFalse(ut.is_mmsi_vessel(0))
        self.assertFalse(ut.is_mmsi_vessel(123))
        self.assertFalse(ut.is_mmsi_vessel(123456789))
        self.assertFalse(ut.is_mmsi_vessel(999999999))
        with self.assertRaises(AssertionError):
            ut.is_mmsi_vessel("string")
        with self.assertRaises(AssertionError):
            ut.is_mmsi_vessel(0.0)

    def test_is_sog_valid(self):
        self.assertTrue(ut.is_sog_valid(0.0))
        self.assertTrue(ut.is_sog_valid(15.1))
        self.assertTrue(ut.is_sog_valid(40.0))
        self.assertFalse(ut.is_sog_valid(-1.0))
        self.assertFalse(ut.is_sog_valid(41.0))
        self.assertTrue(ut.is_sog_valid(41.0, 50.0))
        with self.assertRaises(AssertionError):
            ut.is_sog_valid("string")
        with self.assertRaises(AssertionError):
            ut.is_sog_valid(0)
        with self.assertRaises(AssertionError):
            ut.is_sog_valid(10)
        with self.assertRaises(AssertionError):
            ut.is_sog_valid(-1)

    def test_apply_cog_correction(self):
        self.assertEqual(ut.apply_cog_correction(-409.6), 0.0)
        self.assertEqual(ut.apply_cog_correction(-1.0), 408.6)
        self.assertEqual(ut.apply_cog_correction(0.0), 0.0)
        self.assertEqual(ut.apply_cog_correction(45.0), 45.0)
        self.assertEqual(ut.apply_cog_correction(360.0), 360.0)
        self.assertEqual(ut.apply_cog_correction(720.0), 720.0)
        with self.assertRaises(AssertionError):
            ut.apply_cog_correction("string")
        with self.assertRaises(AssertionError):
            ut.apply_cog_correction(0)
        with self.assertRaises(AssertionError):
            ut.apply_cog_correction(10)
        with self.assertRaises(AssertionError):
            ut.apply_cog_correction(-1)

    def test_is_cog_valid(self):
        self.assertTrue(ut.is_cog_valid(0.0))
        self.assertTrue(ut.is_cog_valid(15.1))
        self.assertFalse(ut.is_cog_valid(-1.0))
        self.assertFalse(ut.is_cog_valid(360.0))
        self.assertFalse(ut.is_cog_valid(361.0))
        with self.assertRaises(AssertionError):
            ut.is_cog_valid("string")
        with self.assertRaises(AssertionError):
            ut.is_cog_valid(0)
        with self.assertRaises(AssertionError):
            ut.is_cog_valid(10)
        with self.assertRaises(AssertionError):
            ut.is_cog_valid(-1)


if __name__ == '__main__':
    unittest.main()
