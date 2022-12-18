import unittest
from src import init


class TestInit(unittest.TestCase):

    def test_is_dir(self):
        result = init.is_dir(r"C:\Users\holec")
        self.assertTrue(result)
