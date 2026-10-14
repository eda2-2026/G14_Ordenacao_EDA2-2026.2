"""Execute com: python3 -m exemplos.demo_bubble"""

from algoritmos.bubble_sort import bubble_sort


if __name__ == "__main__":
    # Cada número representa a posição original de uma coluna da imagem.
    colunas = [3, 0, 4, 1, 2]
    print("Colunas embaralhadas:", colunas)

    def mostrar_troca(estado: list[int]) -> None:
        print("Após troca:         ", estado)

    resultado = bubble_sort(colunas, ao_trocar=mostrar_troca)

    print("Colunas ordenadas:  ", resultado.ordenado)
    print("Comparações:        ", resultado.comparacoes)
    print("Trocas:             ", resultado.trocas)
    print("Passadas:           ", resultado.passadas)
    print("Entrada preservada: ", colunas)
