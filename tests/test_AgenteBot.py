import unittest
from unittest.mock import MagicMock
import sys
import heapq
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AgenteBot import AgenteBot
from typing import Tuple, Callable, List
from unittest.mock import patch

class TestAgenteBot(unittest.TestCase):
    def setUp(self):
        self.agente = AgenteBot()
        self.estado_meta = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.resultados = {
            'clave1': {'tiempo': 30},
            'clave2': {'tiempo': 60},
            'clave3': {'tiempo': 90},
        }
        self.num_estados = 0
        self.clave = "prueba_clave"
        self.estado = (1, 2, 3, 4, 5, 6, 0, 7, 8) 
        self.max_profundidad = 3  
        self.tiempo_limite = 5
    
    def tearDown(self):
        self.agente = None
        self.estado_meta = None
        self.resultados = None
        self.num_estados = None
        self.clave = None
        self.estado = None
        self.max_profundidad = None
        self.tiempo_limite = None

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
    def test_contar_conflictos_filas_error(self):
            estado_invalido = (1, 2, 3) # estado con 8 elems
            with self.assertRaises(ValueError):
                self.agente.contar_conflictos_filas(estado_invalido) 
    def test_contar_conflictos_filas_path_9(self):
        estado = (3, 2, 1, 6, 5, 4, 9, 8, 7) 		
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 18)  
    def test_contar_conflictos_filas_path_8(self):
        estado = (3, 2, 1, 6, 5, 8, 4, 9, 7) 
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 10) 
    def test_contar_conflictos_filas_path_7(self):
        estado = (9, 2, 1, 6, 5, 8, 4, 3, 7) 
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 4) 
    def test_contar_conflictos_filas_path_6(self):
        estado = (0, 2, 3, 6, 0, 4, 9, 8, 0)
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 4)  # Solo hay 2 conflictos (6 y 4), no se ejecuta cuando hay ceros
    def test_contar_conflictos_filas_path_5(self):
        estado = (4, 5, 6, 1, 2, 3, 7, 8, 9)  # 4, 5 y 6 no pertenecen a la fila 0
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 0)  # No hay conflictos contados ya que el if es falso
    def test_contar_conflictos_filas_path_4(self):
        estado = (9, 5, 6, 1, 2, 3, 7, 8, 4)  # 4, 5 y 6 no pertenecen a la fila 0
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 0)  # No hay conflictos contados ya que el if es falso
    def test_contar_conflictos_filas_path_3(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 0)  # No debe haber conflictos en este estado ordenado
    def test_contar_conflictos_filas_path_2(self):
        estado = (1, 3, 0, 4, 5, 6, 7, 8, 2)
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 0)  # No debe haber conflictos en este estado ordenado
    def test_contar_conflictos_filas_path_1(self):
        estado = (2, 1, 3, 6, 5, 4, 0, 8, 7) 
        resultado = self.agente.contar_conflictos_filas(estado)
        self.assertEqual(resultado, 10) 
    
    # fabio 14
    def heuristica_dummy(self, estado: Tuple[int, ...]) -> int:
        return sum(estado)
    def test_inicializar_frontera(self):
        estado_inicial = (1, 2, 3)  # Ejemplo de estado inicial
        frontera = self.agente.inicializar_frontera(estado_inicial, self.heuristica_dummy)
        self.assertEqual(frontera, [(6, (1, 2, 3), [])])  # 1 + 2 + 3 = 6

    # Patrick 12
    def test_contar_conflictos_columnas_sin_conflictos(self):
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.contar_conflictos_columnas(estado), 0)

    def test_contar_conflictos_columnas_con_un_conflicto(self):
        estado = (1, 2, 3, 7, 5, 6, 4, 8, 0)
        self.assertEqual(self.agente.contar_conflictos_columnas(estado), 2)

    def test_contar_conflictos_columnas_con_cero(self):
        estado = (1, 0, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(self.agente.contar_conflictos_columnas(estado), 0)

    def test_contar_conflictos_columnas_multiples_conflictos(self):
        estado = (7, 2, 3, 4, 5, 6, 1, 8, 0)
        self.assertEqual(self.agente.contar_conflictos_columnas(estado), 6)

    # Patrick 15
    def test_frontera_vacia_max_frontera_0(self):
        frontera = [(1, (1, 2), ["A"]), (2, (2, 3), ["B"]), (3, (3, 4), ["C"])]
        max_frontera = 2
        resultado = self.agente.actualizar_max_frontera(frontera, max_frontera)
        self.assertEqual(resultado, 3)


    #Fabio 33
    def heuristica_piezas_fuera_lugar(self, estado):
        return sum(1 for i in range(len(estado)) if estado[i] != self.estado_meta[i] and estado[i] != 0)
    def test_expandir_nodo_Camino1(self):
        estado_inicial = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        camino = []
        frontera = []
        visitados = set()
        g = 0
        self.agente.generar_sucesores = lambda estado: [("mover_abajo", (1, 2, 3, 4, 5, 0, 7, 8, 6))]
        self.agente.expandir_nodo_a_estrella_limitada(estado_inicial, camino, frontera, visitados, self.heuristica_piezas_fuera_lugar, g)
        self.assertEqual(len(frontera), 1, "Frontera no tiene un solo nodo como se esperaba")
        sucesor_esperado = (1, 2, 3, 4, 5, 0, 7, 8, 6)
        nuevo_estado = frontera[0][2]  
        self.assertEqual(nuevo_estado, sucesor_esperado, "El sucesor esperado no está en la frontera")
        self.assertIn(estado_inicial, visitados, "El estado inicial no está en visitados")
        self.assertEqual(len(visitados), 1, "No se visitó un solo estado")
        camino_esperado = ["mover_abajo"]
        self.assertEqual(frontera[0][3], camino_esperado, "El camino no se actualizó")
    def test_no_entra_al_for(self):
        estado_inicial = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Estado inicial del puzzle 3x3
        camino = []
        frontera = []
        visitados = set()
        g = 0
        # Mock de generar_sucesores que devuelve una lista vacía para evitar que el for se ejecute
        self.agente.generar_sucesores = lambda estado: []
        self.agente.expandir_nodo_a_estrella_limitada(estado_inicial, camino, frontera, visitados, self.heuristica_piezas_fuera_lugar, g)
        self.assertEqual(len(frontera), 0, "La frontera no deberia contener nodos, ya que no se generaron sucesores")
        self.assertIn(estado_inicial, visitados, "El estado inicial no se añadió a visitados como se esperaba")
    def test_no_entra_al_if_en_el_for(self):
        estado_inicial = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        camino = []
        frontera = []
        visitados = {(1, 2, 3, 4, 5, 0, 7, 8, 6)} 
        g = 0
        self.agente.generar_sucesores = lambda estado: [("mover_abajo", (1, 2, 3, 4, 5, 0, 7, 8, 6))]
        self.agente.expandir_nodo_a_estrella_limitada(estado_inicial, camino, frontera, visitados, self.heuristica_piezas_fuera_lugar, g)
        self.assertEqual(len(frontera), 0, "La frontera no debería contener nodos, ya que el sucesor estaba en visitados")
        self.assertIn(estado_inicial, visitados, "El estado inicial no se añadió a visitados como se esperaba")

    #fabio 30 TRUE
    @patch.object(AgenteBot, 'busqueda_codiciosa_limitada')
    @patch.object(AgenteBot, 'actualizar_resultados')
    def test_ejecutar_experimento_codiciosa(self, mock_actualizar_resultados, mock_busqueda_codiciosa):
        resultados = {}
        clave = "test_clave"
        algoritmo = "codiciosa"
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)  
        heuristica = lambda x: 0  
        max_profundidad = 10
        tiempo_limite = 1.0
        mock_busqueda_codiciosa.return_value = (['solucion'], 5, 10) 
        self.agente.ejecutar_experimento(resultados, clave, algoritmo, estado, heuristica, max_profundidad, tiempo_limite)
        mock_busqueda_codiciosa.assert_called_once_with(estado, heuristica, max_profundidad, tiempo_limite)
        solucion, nodos_expandidos, max_frontera = mock_busqueda_codiciosa.return_value 
        mock_actualizar_resultados.assert_called_once_with(resultados, clave, solucion, max_frontera, unittest.mock.ANY)

    #FABIO 30 FALSE
    @patch.object(AgenteBot, 'a_estrella_limitada')
    @patch.object(AgenteBot, 'actualizar_resultados')
    def test_ejecutar_experimento_a_estrella(self, mock_actualizar_resultados, mock_a_estrella):
        resultados = {}
        clave = "test_clave"
        algoritmo = "a_estrella"
        estado = (1, 2, 3, 4, 5, 6, 7, 8, 0) 
        heuristica = lambda x: 0 
        max_profundidad = 10
        tiempo_limite = 1.0
        mock_a_estrella.return_value = (['solucion_a'], 10)
        self.agente.ejecutar_experimento(resultados, clave, algoritmo, estado, heuristica, max_profundidad, tiempo_limite)
        mock_a_estrella.assert_called_once_with(estado, heuristica, max_profundidad, tiempo_limite)
        solucion, max_frontera = mock_a_estrella.return_value  # Obtiene los valores devueltos del mock
        mock_actualizar_resultados.assert_called_once_with(resultados, clave, solucion, max_frontera, unittest.mock.ANY)  # El tiempo se pasa como ANY

    # Patrick 16
    def test_extraer_mejor_nodo_multiple_elementos(self):
        """Prueba la extracción cuando la frontera tiene múltiples elementos"""
        estado1 = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        estado2 = (1, 2, 3, 4, 0, 6, 7, 8, 5)
        estado3 = (1, 2, 3, 0, 4, 6, 7, 8, 5)
        
        frontera = [
            (3, estado1, ["arriba"]),
            (1, estado2, ["derecha"]),
            (2, estado3, ["izquierda"])
        ]
        heapq.heapify(frontera)
        
        estado_resultado, camino_resultado = self.agente.extraer_mejor_nodo(frontera)
        
        # Debe extraer el estado2 porque tiene el menor valor heurístico (1)
        self.assertEqual(estado_resultado, estado2)
        self.assertEqual(camino_resultado, ["derecha"])
        self.assertEqual(len(frontera), 2)

    #fabio 28
    @patch.object(AgenteBot, 'generar_estado_valido')
    def test_generar_estados_validos_un_estado(self, mock_generar_estado_valido):
        mock_generar_estado_valido.return_value = (1, 2, 3, 4, 5, 6, 7, 8, 0)  #MOckeo de un estado valido
        agente_bot = AgenteBot()
        estado_generado = agente_bot.generar_estados_validos(1)
        self.assertEqual(len(estado_generado), 1) 
        self.assertEqual(estado_generado[0], (1, 2, 3, 4, 5, 6, 7, 8, 0)) 
        #TESTS ADICIONALES
        self.assertIsInstance(estado_generado, list)  # Comprobar que el resultado es una lista
        self.assertTrue(all(isinstance(i, tuple) and len(i) == 9 for i in estado_generado))  # Verificar que todos los elementos son tuplas de longitud 9
    @patch.object(AgenteBot, 'generar_estado_valido')
    def test_generar_estados_validos_multiple_estados(self, mock_generar_estado_valido):
        mock_generar_estado_valido.side_effect = [
            (1, 2, 3, 4, 5, 6, 7, 8, 0),  
            (2, 1, 3, 4, 5, 6, 7, 8, 0),  
            (3, 1, 2, 4, 5, 6, 7, 8, 0)   
        ]
        estado_generado = self.agente.generar_estados_validos(3) 
        self.assertEqual(len(estado_generado), 3) 
        self.assertEqual(estado_generado[0], (1, 2, 3, 4, 5, 6, 7, 8, 0))  
        self.assertEqual(estado_generado[1], (2, 1, 3, 4, 5, 6, 7, 8, 0))  
        self.assertEqual(estado_generado[2], (3, 1, 2, 4, 5, 6, 7, 8, 0))  
        self.assertEqual(mock_generar_estado_valido.call_count, 3)  # Verificar que se llamó al mock 3 veces
        #TEST ADICIONEALES
        self.assertIn((1, 2, 3, 4, 5, 6, 7, 8, 0), estado_generado)  # Comprobar que un estado válido está en la lista

    #fabio 26
    def test_inicializar_resultados(self):
        resultados = self.agente.inicializar_resultados()
        self.assertIn('codiciosa_h1', resultados)
        self.assertIn('codiciosa_h2', resultados)
        self.assertIn('codiciosa_h3', resultados)
        self.assertIn('a_estrella_h1', resultados)
        self.assertIn('a_estrella_h2', resultados)
        self.assertIn('a_estrella_h3', resultados)
        for key in resultados:
            self.assertEqual(resultados[key]['optimas'], 0)
            self.assertEqual(resultados[key]['tiempo'], 0)
            self.assertEqual(resultados[key]['max_frontera'], 0)
            self.assertEqual(resultados[key]['soluciones'], 0)
            self.assertEqual(resultados[key]['timeout'], 0)

    #fabio 
    def test_actualizar_resultados_path_1(self):
        clave = 'test_clave'
        solucion = ['solucion1']
        max_frontera = 10
        tiempo = 5.0
        self.agente.actualizar_resultados(self.resultados, clave, solucion, max_frontera, tiempo)
        # Verificar que se haya inicializado la clave
        self.assertIn(clave, self.resultados)
        self.assertEqual(self.resultados[clave]['tiempo'], 5.0)
        self.assertEqual(self.resultados[clave]['max_frontera'], 10)
        self.assertEqual(self.resultados[clave]['soluciones'], 1)
        self.assertEqual(self.resultados[clave]['optimas'], 1)
        self.assertEqual(self.resultados[clave]['timeout'], 0)
    def test_actualizar_resultados_path_2(self):
        clave = 'test_clave'
        solucion = []  # Lista vacía, no entra en la condición de `optimas`
        max_frontera = 15
        tiempo = 4.0
        self.agente.actualizar_resultados(self.resultados, clave, solucion, max_frontera, tiempo)
        self.assertIn(clave, self.resultados)
        self.assertEqual(self.resultados[clave]['tiempo'], 4.0)
        self.assertEqual(self.resultados[clave]['max_frontera'], 15)
        self.assertEqual(self.resultados[clave]['soluciones'], 1)
        self.assertEqual(self.resultados[clave]['optimas'], 0)  # No debe incrementarse
        self.assertEqual(self.resultados[clave]['timeout'], 0)
    def test_actualizar_resultados_path_3(self):
        clave = 'test_clave'
        solucion = None  #  debe entrar en el bloque de timeout
        max_frontera = 20
        tiempo = 2.0
        self.agente.actualizar_resultados(self.resultados, clave, solucion, max_frontera, tiempo)
        self.assertIn(clave, self.resultados)
        self.assertEqual(self.resultados[clave]['tiempo'], 2.0)
        self.assertEqual(self.resultados[clave]['max_frontera'], 20)
        self.assertEqual(self.resultados[clave]['soluciones'], 0)  
        self.assertEqual(self.resultados[clave]['optimas'], 0)  
        self.assertEqual(self.resultados[clave]['timeout'], 1)  # Debe incrementarse en 1    
    def test_actualizar_resultados_path_4(self):
        clave = 'test_clave'  
        solucion = None  
        max_frontera = 25
        tiempo = 3.0
        self.agente.actualizar_resultados(self.resultados, clave, solucion, max_frontera, tiempo)
        self.assertIn(clave, self.resultados)
        self.assertEqual(self.resultados[clave]['tiempo'], 3.0)  
        self.assertEqual(self.resultados[clave]['max_frontera'], 25) 
        self.assertEqual(self.resultados[clave]['soluciones'], 0) 
        self.assertEqual(self.resultados[clave]['optimas'], 0)  
        self.assertEqual(self.resultados[clave]['timeout'], 1)  # Debe incrementarse en 1    

    #fabio 30
    def test_promediar_tiempos_path_1(self):
        # Llama a la función
        self.agente.promediar_tiempos(self.resultados, 3)
        # Verifica que los tiempos se han promediado correctamente
        self.assertEqual(self.resultados['clave1']['tiempo'], 10)
        self.assertEqual(self.resultados['clave2']['tiempo'], 20)
        self.assertEqual(self.resultados['clave3']['tiempo'], 30)
if __name__ == '__main__':
    unittest.main()