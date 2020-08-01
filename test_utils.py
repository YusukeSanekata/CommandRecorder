from .utils.io import (
    read_from_storage,
    read_from_text_data,
    write_to_storage,
    add_to_text_data,
)
import sys, os
import unittest

"""
blender -b -P test_operators.py
"""

# fake as a module.
__package__ = os.path.basename(os.path.dirname(__file__))


sample_text = """
askdfjaslf
asdlkfjaslkfja
alskdjflksajflska
asdfsadf


"""


class Test(unittest.TestCase):
    def test_text_data(self):
        add_to_text_data("test", sample_text)
        text = read_from_text_data("test")

        self.assertEqual(sample_text, text)

    def test_storage(self):
        write_to_storage("test", sample_text)
        text = read_from_storage("test")

        self.assertEqual(sample_text, text)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
