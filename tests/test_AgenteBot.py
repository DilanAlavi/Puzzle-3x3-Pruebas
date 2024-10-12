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
        
    def test_generar_estado_valido_multiples_intentos(self):
        estados_no_validos = 2
        call_count = 0
        
        def es_solucionable_mock(estado):
            nonlocal call_count
            call_count += 1
            return call_count > estados_no_validos  # El tercer intento es válido
        self.agente.es_solucionable = MagicMock(side_effect=es_solucionable_mock)
        estado = self.agente.generar_estado_valido()
        self.assertIsInstance(estado, tuple)
        self.assertEqual(len(estado), 9)
        self.assertTrue(all(0 <= n <= 8 for n in estado))
        self.assertEqual(self.agente.es_solucionable.call_count, 3)
        
    def test_estado_vacio_o_un_elemento(self):
        self.assertTrue(self.agente.es_solucionable([]))
        self.assertTrue(self.agente.es_solucionable([0]))
        self.assertTrue(self.agente.es_solucionable([1]))


    
if __name__ == '__main__':
    unittest.main()