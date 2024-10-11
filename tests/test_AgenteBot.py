import unittest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AgenteBot import AgenteBot

class TestAgenteBot(unittest.TestCase):
    def setUp(self):
        self.agente = AgenteBot()

    def test_init(self):
        self.assertEqual(self.agente.estado_meta, (1, 2, 3, 4, 5, 6, 7, 8, 0))
    
if __name__ == '__main__':
    unittest.main()