import unittest
import os
import sys
import uuid

sys.path.append('../')
from boat import Boat

class BoatTest(unittest.TestCase):

    def test_id(self):
        id = uuid.uuid4()
        b = Boat(id)
        self.assertEqual(id, b.id)



if __name__ == '__main__':
	unittest.main(verbosity=2)