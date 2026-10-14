import random
import unittest

from algoritmos.bubble_sort import bubble_sort


class TestBubbleSort(unittest.TestCase):
    def test_exemplo_colunas(self) -> None:
        entrada = [3, 0, 4, 1, 2]
        resultado = bubble_sort(entrada)
        self.assertEqual(resultado.ordenado, [0, 1, 2, 3, 4])
        self.assertEqual(resultado.comparacoes, 9)
        self.assertEqual(resultado.trocas, 5)
        self.assertEqual(resultado.passadas, 3)
        self.assertEqual(entrada, [3, 0, 4, 1, 2])

    def test_lista_vazia(self) -> None:
        resultado = bubble_sort([])
        self.assertEqual(resultado.ordenado, [])
        self.assertEqual((resultado.comparacoes, resultado.trocas, resultado.passadas), (0, 0, 0))

    def test_um_elemento(self) -> None:
        resultado = bubble_sort([7])
        self.assertEqual(resultado.ordenado, [7])
        self.assertEqual(resultado.comparacoes, 0)

    def test_ja_ordenada_encerra_antecipadamente(self) -> None:
        resultado = bubble_sort([0, 1, 2, 3, 4])
        self.assertEqual(resultado.ordenado, [0, 1, 2, 3, 4])
        self.assertEqual(resultado.comparacoes, 4)
        self.assertEqual(resultado.trocas, 0)
        self.assertEqual(resultado.passadas, 1)

    def test_ordem_inversa(self) -> None:
        resultado = bubble_sort([4, 3, 2, 1])
        self.assertEqual(resultado.ordenado, [1, 2, 3, 4])
        self.assertEqual(resultado.trocas, 6)

    def test_repetidos_e_negativos(self) -> None:
        self.assertEqual(bubble_sort([2, -1, 2, 0, -1]).ordenado, [-1, -1, 0, 2, 2])

    def test_callback_recebe_copias_independentes(self) -> None:
        estados: list[list[int]] = []
        resultado = bubble_sort([2, 1, 0], ao_trocar=estados.append)
        self.assertEqual(estados, [[1, 2, 0], [1, 0, 2], [0, 1, 2]])
        self.assertEqual(len(estados), resultado.trocas)
        estados[0][0] = 99
        self.assertEqual(resultado.ordenado, [0, 1, 2])
        self.assertEqual(estados[1], [1, 0, 2])

    def test_compara_com_sorted_varias_entradas(self) -> None:
        gerador = random.Random(2026)
        for tamanho in range(0, 21):
            for _ in range(10):
                entrada = [gerador.randint(-20, 20) for _ in range(tamanho)]
                with self.subTest(entrada=entrada):
                    self.assertEqual(bubble_sort(entrada).ordenado, sorted(entrada))


if __name__ == "__main__":
    unittest.main()
