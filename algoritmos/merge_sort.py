from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class ResultadoMergeSort:

    ordenado: list[int]
    comparacoes: int
    escritas: int


def merge_sort(
    lst: list[int],
    *,
    ao_escrever: Callable[[int, int], None] | None = None,
    ao_comparar: Callable[[], None] | None = None,
) -> ResultadoMergeSort:

    vetor = lst.copy()
    comparacoes = 0
    escritas = 0

    def ordenar(inicio: int, fim: int) -> None:
        nonlocal comparacoes, escritas
        if fim - inicio < 2:
            return

        # Divide ao meio e ordena cada metade.
        meio = (inicio + fim) // 2
        ordenar(inicio, meio)
        ordenar(meio, fim)

        # Intercala as duas metades já ordenadas de volta no vetor.
        esquerda = vetor[inicio:meio]
        direita = vetor[meio:fim]
        for k in range(inicio, fim):
            if esquerda and direita:
                comparacoes += 1
                if ao_comparar is not None:
                    ao_comparar()
                usar_esquerda = esquerda[0] <= direita[0]
            else:
                usar_esquerda = bool(esquerda)

            vetor[k] = esquerda.pop(0) if usar_esquerda else direita.pop(0)
            escritas += 1
            if ao_escrever is not None:
                ao_escrever(k, vetor[k])

    ordenar(0, len(vetor))

    return ResultadoMergeSort(ordenado=vetor, comparacoes=comparacoes, escritas=escritas)
