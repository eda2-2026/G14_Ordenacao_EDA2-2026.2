from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class ResultadoBubbleSort:

    ordenado: list[int]
    comparacoes: int
    trocas: int
    passadas: int


def bubble_sort(
    lst: list[int],
    *,
    ao_trocar: Callable[[list[int]], None] | None = None,
) -> ResultadoBubbleSort:

    vetor = lst.copy()
    comparacoes = 0
    trocas = 0
    passadas = 0

    # O último elemento da parte ativa fica em sua posição definitiva a cada passada.
    for fim in range(len(vetor) - 1, 0, -1):
        passadas += 1
        houve_troca = False

        for i in range(fim):
            comparacoes += 1
            if vetor[i] > vetor[i + 1]:
                vetor[i], vetor[i + 1] = vetor[i + 1], vetor[i]
                trocas += 1
                houve_troca = True

                if ao_trocar is not None:
                    ao_trocar(vetor.copy())

        # Se não houve trocas, tudo já está ordenado.
        if not houve_troca:
            break

    return ResultadoBubbleSort(
        ordenado=vetor,
        comparacoes=comparacoes,
        trocas=trocas,
        passadas=passadas,
    )
