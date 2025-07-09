import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.moe.moe_inference import moe_retrieve

class TestMoeInference(unittest.TestCase):

    def test_import(self):
        self.assertTrue(callable(moe_retrieve))

if __name__ == '__main__':
    unittest.main()