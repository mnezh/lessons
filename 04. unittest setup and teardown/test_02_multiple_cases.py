import unittest
import os
from datetime import datetime


class TestFile(unittest.TestCase):
    def test_file_exists(self):
        file_name = "file.txt"
        print(f"Creating file {file_name}")
        with open(file_name, "w") as f:
            f.write("text")
        self.assertTrue(os.path.exists(file_name))

    def test_is_file(self):
        file_name = "file.txt"
        print(f"Creating file {file_name}")
        with open(file_name, "w") as f:
            f.write("text")
        self.assertTrue(os.path.isfile(file_name))

    def test_is_4_bytes_long(self):
        file_name = "file.txt"
        print(f"Creating file {file_name}")
        with open(file_name, "w") as f:
            f.write("text")
        self.assertEqual(os.path.getsize(file_name), 4)

    def test_is_created_today(self):
        file_name = "file.txt"
        print(f"Creating file {file_name}")
        with open(file_name, "w") as f:
            f.write("text")
        created_time = datetime.fromtimestamp(os.path.getmtime(file_name))
        self.assertEqual(datetime.today().date(), created_time.date())
