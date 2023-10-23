import unittest
import os
from datetime import datetime


class TestFileClassSetup(unittest.TestCase):
    # executed before the first test
    @classmethod
    def setUpClass(cls) -> None:
        cls.file_name = "file.txt"
        print(f"setUpClass: Creating file {cls.file_name}")
        with open(cls.file_name, "w") as f:
            f.write("text")

    # executed after all tests are finished
    @classmethod
    def tearDownClass(cls) -> None:
        print(f"tearDownClass: Deleting file {cls.file_name}")
        os.remove(cls.file_name)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.file_name))

    def test_is_file(self):
        self.assertTrue(os.path.isfile(self.file_name))

    def test_is_4_bytes_long(self):
        self.assertEqual(os.path.getsize(self.file_name), 4)

    def test_is_created_today(self):
        created_time = datetime.fromtimestamp(os.path.getmtime(self.file_name))
        self.assertEqual(datetime.today().date(), created_time.date())
