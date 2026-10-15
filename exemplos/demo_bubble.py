"""Execute com: python3 -m exemplos.demo_bubble"""

from algoritmos.bubble_sort import bubble_sort


if __name__ == "__main__":
    # Cada número representa a posição original de uma coluna da imagem.
    colunas = [3, 0, 4, 1, 2]
    print("Colunas embaralhadas:", colunas)

    def mostrar_escrita(posicao: int, valor: int) -> None:
        print(f"Escreveu {valor} na posição {posicao}")

    resultado = bubble_sort(colunas, ao_escrever=mostrar_escrita)

    print("Colunas ordenadas:  ", resultado.ordenado)
    print("Comparações:        ", resultado.comparacoes)
    print("Trocas:             ", resultado.trocas)
    print("Escritas:           ", resultado.escritas)
    print("Passadas:           ", resultado.passadas)
    print("Entrada preservada: ", colunas)
