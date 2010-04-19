import unittest2

from coincidence.timeout import timelimited, TimeoutException

def endless():
    while True:
        pass

def ends(x):
    return x**2

def raises():
    raise Exception("This is a test")

class TimeoutTests(unittest2.TestCase):

    def test_endless(self):
        self.assertRaises(TimeoutException, timelimited, 1, endless)

    def test_ending(self):
        self.assertEqual(timelimited(1, ends, 2), 2**2)

    def test_raising(self):
        self.assertRaisesRegexp(Exception, 'test', timelimited, 1, raises)
