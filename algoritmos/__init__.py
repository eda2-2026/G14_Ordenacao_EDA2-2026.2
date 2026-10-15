"""Algoritmos de ordenação do projeto EDA2."""

from algoritmos.bubble_sort import bubble_sort
from algoritmos.counting_sort import counting_sort
from algoritmos.merge_sort import merge_sort

ALGORITMOS = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Counting Sort": counting_sort,
}
