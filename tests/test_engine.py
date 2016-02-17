import unittest, sqlite3
from engine.engine import Engine

class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_auth(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestEngine)
unittest.TextTestRunner(verbosity=2).run(suite)
