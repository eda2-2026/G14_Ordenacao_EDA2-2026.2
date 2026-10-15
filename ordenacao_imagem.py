"""Execute com: python ordenacao_imagem.py"""

import random
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk

from algoritmos import ALGORITMOS

TAMANHO = 480
GRADE = 16
LADO = TAMANHO // GRADE
IMAGEM = Path(__file__).parent / "assets" / "nunkiditos.jpg"

# Escritas reproduzidas por quadro em cada posição da velocidade (só a primeira desliza).
LOTES = (2, 8, 32, 128, 512, 2048)


def cortar_pedacos() -> list[Image.Image]:
    """Corta a imagem em GRADE x GRADE pedaços; o pedaço k (linha a linha) traz o número k."""
    with Image.open(IMAGEM) as original:
        imagem = original.convert("RGB").resize((TAMANHO, TAMANHO))

    fonte = ImageFont.load_default(size=12)
    pedacos = []
    for numero in range(GRADE * GRADE):
        linha, coluna = divmod(numero, GRADE)
        x, y = coluna * LADO, linha * LADO
        pedaco = imagem.crop((x, y, x + LADO, y + LADO))
        ImageDraw.Draw(pedaco).text(
            (2, 2), str(numero), fill="white", stroke_width=1, stroke_fill="black", font=fonte
        )
        pedacos.append(pedaco)
    return pedacos


def posicao(casa: int) -> tuple[int, int]:
    return (casa % GRADE) * LADO, (casa // GRADE) * LADO


class App:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        raiz.title("Ordenação com imagem")
        self.fotos = [ImageTk.PhotoImage(p) for p in cortar_pedacos()]

        self.canvas = tk.Canvas(raiz, width=TAMANHO, height=TAMANHO, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.seletor = ttk.Combobox(raiz, values=list(ALGORITMOS), state="readonly", width=14)
        self.seletor.current(0)
        self.seletor.grid(row=1, column=0, padx=4, pady=4)
        self.botao_embaralhar = tk.Button(raiz, text="Embaralhar", command=self.embaralhar)
        self.botao_embaralhar.grid(row=1, column=1)
        self.botao_ordenar = tk.Button(raiz, text="Ordenar", command=self.ordenar)
        self.botao_ordenar.grid(row=1, column=2)
        self.velocidade = tk.Scale(
            raiz, from_=1, to=len(LOTES), orient="horizontal", label="Velocidade", showvalue=False
        )
        self.velocidade.set(4)
        self.velocidade.grid(row=1, column=3, padx=4)
        self.contadores = tk.Label(raiz)
        self.contadores.grid(row=2, column=0, columnspan=4, pady=4)

        self.em_andamento = False
        self.embaralhar()

    def embaralhar(self) -> None:
        if self.em_andamento:
            return
        self.vetor = list(range(GRADE * GRADE))
        while self.vetor == sorted(self.vetor):
            random.shuffle(self.vetor)

        self.canvas.delete("all")
        self.itens = [0] * len(self.vetor)  # itens[numero] = id do pedaço no canvas
        for casa, numero in enumerate(self.vetor):
            self.itens[numero] = self.canvas.create_image(
                *posicao(casa), image=self.fotos[numero], anchor="nw"
            )
        self.contadores.config(text="Comparações: -     Escritas: -")

    def ordenar(self) -> None:
        if self.em_andamento:
            return
        # Sequência do que o algoritmo fez: None = uma comparação, (pos, valor) = uma escrita.
        self.eventos: list[tuple[int, int] | None] = []
        self.resultado = ALGORITMOS[self.seletor.get()](
            self.vetor,
            ao_escrever=lambda pos, valor: self.eventos.append((pos, valor)),
            ao_comparar=lambda: self.eventos.append(None),
        )
        self.indice = 0
        self.comparacoes = 0
        self.escritas = 0
        self._mostrar_contadores()
        self._bloquear(True)
        self._avancar()

    def _mostrar_contadores(self) -> None:
        self.contadores.config(
            text=f"Comparações: {self.comparacoes}     Escritas: {self.escritas}"
        )

    def _bloquear(self, bloqueado: bool) -> None:
        self.em_andamento = bloqueado
        estado = tk.DISABLED if bloqueado else tk.NORMAL
        self.botao_embaralhar.config(state=estado)
        self.botao_ordenar.config(state=estado)
        self.seletor.config(state="disabled" if bloqueado else "readonly")

    def _avancar(self) -> None:
        if self.indice >= len(self.eventos):
            self.vetor = list(self.resultado.ordenado)
            self._bloquear(False)
            return

        # Consome eventos até juntar `tamanho` escritas; as comparações no meio só sobem o contador.
        tamanho = LOTES[int(self.velocidade.get()) - 1]
        lote = []
        consumidos = 0
        while (
            self.indice < len(self.eventos) and len(lote) < tamanho and consumidos < 4 * tamanho
        ):
            evento = self.eventos[self.indice]
            self.indice += 1
            consumidos += 1
            if evento is None:
                self.comparacoes += 1
            else:
                lote.append(evento)
        self.escritas += len(lote)
        self._mostrar_contadores()

        if lote and tamanho == LOTES[0]:
            movimentos = []
            for pos, valor in lote:
                item = self.itens[valor]
                self.canvas.tag_raise(item)
                movimentos.append((item, *self.canvas.coords(item), *posicao(pos)))
            self._deslizar(movimentos, 1)
        else:
            for pos, valor in lote:
                self.canvas.coords(self.itens[valor], *posicao(pos))
            self.raiz.after(15, self._avancar)

    def _deslizar(self, movimentos: list, quadro: int, quadros: int = 8) -> None:
        t = quadro / quadros
        for item, x0, y0, x1, y1 in movimentos:
            self.canvas.coords(item, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
        if quadro < quadros:
            self.raiz.after(15, self._deslizar, movimentos, quadro + 1)
        else:
            self.raiz.after(15, self._avancar)


if __name__ == "__main__":
    raiz = tk.Tk()
    App(raiz)
    raiz.mainloop()
