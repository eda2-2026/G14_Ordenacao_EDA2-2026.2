from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class ResultadoCountingSort:

    ordenado: list[int]
    comparacoes: int
    escritas: int


def counting_sort(
    lst: list[int],
    *,
    ao_escrever: Callable[[int, int], None] | None = None,
    ao_comparar: Callable[[], None] | None = None,  # aceito por compatibilidade; nunca é chamado
) -> ResultadoCountingSort:

    vetor = lst.copy()
    escritas = 0

    if vetor:
        # Conta quantas vezes cada valor aparece (o menor valor fica na posição 0).
        menor = min(vetor)
        contagem = [0] * (max(vetor) - menor + 1)
        for valor in vetor:
            contagem[valor - menor] += 1

        # Reescreve o vetor em ordem, repetindo cada valor pelo número de vezes contado.
        posicao = 0
        for valor, quantidade in enumerate(contagem, start=menor):
            for _ in range(quantidade):
                vetor[posicao] = valor
                escritas += 1
                if ao_escrever is not None:
                    ao_escrever(posicao, valor)
                posicao += 1

    # O Counting Sort não compara elementos entre si.
    return ResultadoCountingSort(ordenado=vetor, comparacoes=0, escritas=escritas)
