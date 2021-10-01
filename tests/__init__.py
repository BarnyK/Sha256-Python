import unittest

def make_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    return suite