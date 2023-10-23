import unittest
import os
from datetime import datetime
import tempfile

test_dir = ""


# executed before first test and class setup in this file
def setUpModule():
    global test_dir
    test_dir = tempfile.mkdtemp()
    print(f"setUpModule: Created dir {test_dir}")


# executed after all tests and class tear downs in this file are finished
def tearDownModule():
    global test_dir
    print(f"tearDownModule: Deleting dir {test_dir}")
    os.rmdir(test_dir)


class TestFileClassSetup(unittest.TestCase):
    # executed before the first test
    @classmethod
    def setUpClass(cls) -> None:
        cls.file_name = os.path.join(test_dir, "file.txt")
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


class TestDirectory(unittest.TestCase):
    # executed before the first test
    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_name = os.path.join(test_dir, "test_dir")
        print(f"setUpClass: Creating dir {cls.dir_name}")
        os.mkdir(cls.dir_name)

    # executed after all tests are finished
    @classmethod
    def tearDownClass(cls) -> None:
        print(f"tearDownClass: Deleting dir {cls.dir_name}")
        os.rmdir(cls.dir_name)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.dir_name))

    def test_is_created_today(self):
        created_time = datetime.fromtimestamp(os.path.getmtime(self.dir_name))
        self.assertEqual(datetime.today().date(), created_time.date())
