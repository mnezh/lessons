import unittest
import os


class TestFileExist(unittest.TestCase):
    def test_created_file_exists(self):
        file_name = "file.txt"
        print(f"Creating file {file_name}")
        with open(file_name, "w") as f:
            f.write("text")
        self.assertTrue(os.path.exists(file_name))
