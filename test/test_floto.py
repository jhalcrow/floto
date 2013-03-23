import unittest
import floto

class DisplayTest(unittest.TestCase):

    def setUp(self):
        self.app = floto.create_app()

    def test_get_photo(self):
        client = self.app.test_client()

if __name__ == '__main__':
    unittest.main()