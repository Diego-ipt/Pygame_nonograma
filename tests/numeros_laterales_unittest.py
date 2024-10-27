import unittest
import sys
import os

# Add the parent directory of 'nonograma_core' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nonograma_core.Logica.nonograma_numeros import *


# test_nonograma_numeros.py
class TestProcesarMatriz(unittest.TestCase):
    
    def test_matriz_todos_ceros(self):
        matriz = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        esperado = ([(), (), ()], [(), (), ()])
        self.assertEqual(procesar_matriz(matriz), esperado)

    def test_matriz_todos_unos(self):
        matriz = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        esperado = ([(3,), (3,), (3,)], [(3,), (3,), (3,)])
        self.assertEqual(procesar_matriz(matriz), esperado)

    def test_matriz_mixta(self):
        matriz = [
            [1, 0, 1, 1, 0],
            [0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0]
        ]
        esperado = (
           [(1, 2), (1, 1), (3,), (3,), (1, 1)],
           [(1, 1, 1), (2,), (1, 2), (1, 2), (1, 1)]
        )
        self.assertEqual(procesar_matriz(matriz), esperado)

    def test_matriz_vacia(self):
        matriz = []
        esperado = ([], [])
        self.assertEqual(procesar_matriz(matriz), esperado)

if __name__ == '__main__':
    unittest.main()