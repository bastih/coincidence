import unittest2

from coincidence.isolation import isolate, isolate_from, IsolationException

class IsolationTests(unittest2.TestCase):

    def test_without_extra_imports(self):
        @isolate
        def plain():
            return "test"
        assert plain() == "test"

    def test_with_imports(self):
        import math
        @isolate_from("math")
        def isolated_from_math_imports():
            raise Exception("Method was called although os was imported")
        self.assertRaises(IsolationException, isolated_from_math_imports)

