import unittest
import os
from datetime import datetime


class TestFileSetup(unittest.TestCase):
    # executed before each test
    def setUp(self) -> None:
        self.file_name = "file.txt"
        print(f"setUp: Creating file {self.file_name}")
        with open(self.file_name, "w") as f:
            f.write("text")

    # executed after each test
    def tearDown(self) -> None:
        print(f"tearDown: Deleting file {self.file_name}")
        os.remove(self.file_name)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.file_name))

    def test_is_file(self):
        self.assertTrue(os.path.isfile(self.file_name))

    def test_is_4_bytes_long(self):
        self.assertEqual(os.path.getsize(self.file_name), 4)

    def test_is_created_today(self):
        created_time = datetime.fromtimestamp(os.path.getmtime(self.file_name))
        self.assertEqual(datetime.today().date(), created_time.date())
