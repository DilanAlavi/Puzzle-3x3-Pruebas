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
        
    def test_generar_estado_valido_primer_intento(self):
        self.agente.es_solucionable = MagicMock(return_value=True)
        estado = self.agente.generar_estado_valido()
        self.assertIsInstance(estado, tuple)
        self.assertEqual(len(estado), 9)
        self.assertTrue(all(0 <= n <= 8 for n in estado))
        self.assertEqual(self.agente.es_solucionable.call_count, 1)
    
if __name__ == '__main__':
    unittest.main()