import unittest
import sys
from src import *


class TestClick(unittest.TestCase):

    def test_get_urls(self):
        self.assertTrue(get_urls(sys.argv[1]))
