import unittest
import init


class TestInit(unittest.TestCase):

    def test_is_dir(self):
        result_true = init.is_dir(r"C:\Users\holec")
        result_false = init.is_dir(r"C:\Users\hole")
        self.assertTrue(result_true)
        self.assertFalse(result_false)

    def test_is_file(self):
        result_true = init.is_file(r"C:\Users\holec\Desktop\plex_bcup.txt")
        result_false = init.is_file(r"C:\Users\holec\Desktop\BIP32.txt")
        self.assertTrue(result_true)
        self.assertFalse(result_false)

    def test_read_file(self):
        result = init.read_file(r"C:\Users\holec\Desktop\urls.txt")
        result_expected: list = ['url1', 'url2', 'url3', 'url4']
        self.assertListEqual(result, result_expected)
