import unittest

from jwapiserver import config


class TestConfig(unittest.TestCase):

    def test_read(self):
        print(config.DEBUG)
        print(config.PATH_DATA)
