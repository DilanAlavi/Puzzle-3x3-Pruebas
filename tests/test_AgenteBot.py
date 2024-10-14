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
        
    def test_estado_sin_inversiones(self):
        self.assertTrue(self.agente.es_solucionable([1, 2, 3, 4, 0]))
        self.assertTrue(self.agente.es_solucionable([0, 1, 2, 3, 4]))
    def test_estado_con_inversiones(self):
        self.assertFalse(self.agente.es_solucionable([2, 1, 3, 4, 0]))  
        self.assertFalse(self.agente.es_solucionable([3, 2, 1, 4, 0])) 
        self.assertTrue(self.agente.es_solucionable([4, 3, 2, 1, 0]))
          
    def test_generar_sucesores_centro(self):
        estado = (1, 2, 3, 4, 0, 5, 6, 7, 8)
        sucesores = self.agente.generar_sucesores(estado)
        self.assertEqual(len(sucesores), 4) 
        movimientos_esperados = set(['arriba', 'abajo', 'izquierda', 'derecha'])
        movimientos_obtenidos = set(mov for mov, _ in sucesores)
        self.assertEqual(movimientos_esperados, movimientos_obtenidos)
        
    def test_generar_sucesores_esquina(self):
        estado = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        sucesores = self.agente.generar_sucesores(estado)
        self.assertEqual(len(sucesores), 2) 
        movimientos_esperados = set(['abajo', 'derecha'])
        movimientos_obtenidos = set(mov for mov, _ in sucesores)
        self.assertEqual(movimientos_esperados, movimientos_obtenidos)
        
    def test_estados_resultantes(self):
        estado = (1, 2, 3, 4, 0, 5, 6, 7, 8)
        sucesores = self.agente.generar_sucesores(estado)
        estados_esperados = [
            (1, 0, 3, 4, 2, 5, 6, 7, 8),  
            (1, 2, 3, 4, 7, 5, 6, 0, 8),  
            (1, 2, 3, 0, 4, 5, 6, 7, 8),  
            (1, 2, 3, 4, 5, 0, 6, 7, 8)  
        ]
        estados_obtenidos = [estado for _, estado in sucesores]
        self.assertEqual(set(estados_esperados), set(estados_obtenidos))

    def test_estado_resuelto(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        sucesores = self.agente.generar_sucesores(estado)
        self.assertEqual(len(sucesores), 2)  
        movimientos_esperados = set(['arriba', 'izquierda'])
        movimientos_obtenidos = set(mov for mov, _ in sucesores)
        self.assertEqual(movimientos_esperados, movimientos_obtenidos)
        
    def test_vacio_al_inicio(self):
        estado = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual(self.agente.encontrar_vacio(estado), 0)

    def test_vacio_al_final(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.encontrar_vacio(estado), 8)

    def test_estado_con_un_elemento(self):
        estado = (0,)
        self.assertEqual(self.agente.encontrar_vacio(estado), 0)
        
    def test_movimientos_validos_centro(self):
        indice_vacio = 4  # Posición central del tablero
        movimientos_esperados = [
            ('arriba', -3),
            ('abajo', 3),
            ('izquierda', -1),
            ('derecha', 1)
        ]
        movimientos_obtenidos = self.agente.obtener_movimientos_validos(indice_vacio)
        self.assertEqual(set(movimientos_obtenidos), set(movimientos_esperados))
        self.assertEqual(len(movimientos_obtenidos), 4)
        
    def test_intercambiar(self):
        estado_inicial = [1, 0, 2, 3, 4, 5, 6, 7, 8]
        indice_vacio = 1
        offset = 1
        estado_esperado = (1, 2, 0, 3, 4, 5, 6, 7, 8)
        resultado = self.agente.intercambiar(estado_inicial, indice_vacio, offset)
        self.assertEqual(resultado, estado_esperado)
    def test_aplicar_movimientos(self):
        estado_inicial = (1, 2, 3, 4, 0, 5, 6, 7, 8)
        indice_vacio = 4
        movimientos = [
            ('arriba', -3),
            ('abajo', 3),
            ('izquierda', -1),
            ('derecha', 1)
        ]

        sucesores = self.agente.aplicar_movimientos(estado_inicial, indice_vacio, movimientos)
        # Verificar que se generaron 4 sucesores
        self.assertEqual(len(sucesores), 4)
        sucesores_esperados = [
            ('arriba', (1, 0, 3, 4, 2, 5, 6, 7, 8)),
            ('abajo', (1, 2, 3, 4, 7, 5, 6, 0, 8)),
            ('izquierda', (1, 2, 3, 0, 4, 5, 6, 7, 8)),
            ('derecha', (1, 2, 3, 4, 5, 0, 6, 7, 8))
        ]
        self.assertEqual(set(sucesores), set(sucesores_esperados))
        
    def test_estado_ordenado(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.heuristica_piezas_fuera_lugar(estado), 0)

    def test_estado_completamente_desordenado(self):
        estado = (8, 7, 6, 5, 4, 3, 2, 1, 0)
        self.assertEqual(self.agente.heuristica_piezas_fuera_lugar(estado), 8)
    def test_estado_ordenado(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.heuristica_distancia_manhattan(estado), 12)
    def test_estado_completamente_desordenado(self):
        estado = (8, 7, 6, 5, 4, 3, 2, 1, 0)
        self.assertEqual(self.agente.heuristica_distancia_manhattan(estado), 20)
        
    def test_heuristica_secuencia_lineal_conflictos_con_conflictos(self):
        estado_con_conflictos = (2, 1, 3, 4, 5, 6, 8, 7, 0)
        h_conflictos = self.agente.heuristica_secuencia_lineal_conflictos(estado_con_conflictos)
        h_manhattan = self.agente.heuristica_distancia_manhattan(estado_con_conflictos)
        self.assertGreater(h_conflictos, h_manhattan)
    def test_heuristica_secuencia_lineal_conflictos_siempre_mayor_igual_manhattan(self):
        estado_aleatorio = (3, 1, 2, 4, 0, 5, 6, 7, 8)
        h_slc = self.agente.heuristica_secuencia_lineal_conflictos(estado_aleatorio)
        h_manhattan = self.agente.heuristica_distancia_manhattan(estado_aleatorio)
        self.assertGreaterEqual(h_slc, h_manhattan)


    # fabio 11
    def test_contar_conflictos_filas_no_conflictos(self):
        estado = (1, 2, 0, 4, 5, 6, 7, 8, 0)
        conflictos = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(conflictos, 0)
    def test_contar_conflictos_filas_caminos(self):
        estado = (1, 0, 2, 4, 5, 0, 7, 8, 0)
        conflictos = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(conflictos, 0)
    def test_contar_conflictos_filas_caminos3(self):
        estado = (1, 2, 0, 0, 5, 0, 7, 8, 0)
        conflictos = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(conflictos, 0)

    # Patrick 12

    def test_contar_conflictos_columnas_sin_conflictos(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.contar_conflictos_columnas(estado), 0)

if __name__ == '__main__':
    unittest.main()