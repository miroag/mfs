import os

import pytest


@pytest.fixture
def testdata():
    """
    Simple fixture to return reference data
    :return:
    """

    class TestData():
        def __init__(self):
            self.datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

        def fn(self, fn):
            return os.path.join(self.datadir, fn)

        def textdata(self, fn):
            with open(self.fn(fn), encoding='utf8') as f:
                return f.read()

    return TestData()
