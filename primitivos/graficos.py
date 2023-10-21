from primitivos import *
from tkinter import Label


def normaliza(coordenada: dict) -> dict:
    x = coordenada['x'] / 800
    y = coordenada['y'] / 600

    return {"x": x, "y": y}


def converte(cor_rgb: str) -> dict:
    dict_rgb = {}
    cor_rgb = cor_rgb[1:]
    cores = [cor_rgb[i:i + 2] for i in range(0, 5, 2)]

    for cor, valor in zip(['r', 'g', 'b'], cores):
        dict_rgb[cor] = int(valor, 16)

    return dict_rgb


class PontoGr(Ponto):
    _id = 0

    def __init__(self, x=0, y=0, cor='#000000', width=None):
        super().__init__(x, y)
        self.cor = cor
        self.width = width

        PontoGr._id += 1
        self.id = f'ponto_{PontoGr._id}'

        self.tag = None

    def __add__(self, numero):
        return PontoGr(self.x + numero, self.y + numero, self.cor, self.width)

    def __sub__(self, outro):
        # retorna a distancia entre os dois pontos
        if isinstance(outro, PontoGr):
            d = math.sqrt((self.y - outro.y) ** 2 + (self.x - outro.x) ** 2)
            return d
        return PontoGr(self.x - outro, self.y - outro, self.cor, self.width)

    def copiar(self):
        return PontoGr(x=self.x, y=self.y, cor=self.cor, width=self.width)

    def desenhaPonto(self, canvas):
        raio = self.width
        canvas.create_oval(
            (self.x - raio, self.y - raio),
            (self.x + raio, self.y + raio),
            fill=self.cor, outline=self.cor)

    def __del__(self):
        PontoGr._id -= 1

    def apagar(self, canvas):
        self.cor = '#FFFFFF'
        self.desenhaPonto(canvas)

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='p' + self.id[6:], bg='white')

            self.tag.place(x=self.x + self.width + 5, y=self.y - 5)
        else:
            if self.tag:
                self.tag.place_forget()

    def info(self) -> dict:
        return {'id': self.id, 'esp': self.width, **normaliza({"x": self.x, "y": self.y}), 'cor': converte(self.cor)}


class RetaGr(Reta):
    _id = 0

    def __init__(self, p1, p2, cor, width):
        super().__init__(p1, p2)
        self.cor = cor
        self.width = width

        RetaGr._id += 1
        self.id = f"reta_{RetaGr._id}"

        self.tag = None

    def desenhaReta(self, canvas):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        steps = round(1 if 0 <= steps <= 1 else steps)

        incremento_x = dx / float(steps)
        incremento_y = dy / float(steps)

        ponto_inicial = PontoGr(self.p1.x, self.p1.y, self.cor, self.width)
        for v in range(0, steps):
            ponto_inicial.x += incremento_x
            ponto_inicial.y += incremento_y
            ponto_inicial.desenhaPonto(canvas)

    def apagar(self, canvas):
        self.p1.cor = '#FFFFFF'
        self.desenhaReta(canvas)

    def __del__(self):
        RetaGr._id -= 1

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='r' + self.id[5:], bg='white')

            self.tag.place(x=self.p2.x + self.width + 5, y=self.p2.y - 5)
        else:
            if self.tag:
                self.tag.place_forget()


class RetanguloGr(Retangulo):
    _id = 0

    def __init__(self, p1, p2, cor, width):
        super().__init__(p1, p2)
        self.cor = cor
        self.width = width

        RetanguloGr._id += 1
        self.id = f"retang_{RetanguloGr._id}"

        self.tag = None

    def desenhaRetangulo(self, canvas):
        RetaGr(self.p1, PontoGr(self.p1.x, self.p2.y, self.cor, self.width), self.cor, self.width).desenhaReta(canvas)
        RetaGr(PontoGr(self.p1.x, self.p2.y, self.cor, self.width), self.p2, self.cor, self.width).desenhaReta(canvas)
        RetaGr(self.p2, PontoGr(self.p2.x, self.p1.y, self.cor, self.width), self.cor, self.width).desenhaReta(canvas)
        RetaGr(PontoGr(self.p2.x, self.p1.y, self.cor, self.width),
               PontoGr(self.p1.x, self.p1.y, self.cor, self.width), self.cor, self.width).desenhaReta(canvas)

    def apagar(self, canvas):
        self.p1.cor = '#FFFFFF'
        self.p2.cor = '#FFFFFF'
        self.desenhaRetangulo(canvas)

    def __del__(self):
        RetanguloGr._id -= 1

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='rtg' + self.id[7:], bg='white')

            self.tag.place(x=self.p2.x + self.width + 5, y=self.p2.y + self.width + 3)
        else:
            if self.tag:
                self.tag.place_forget()


class TrianguloGr(Triangulo):
    _id = 0

    def __init__(self, pontos, cor, width):
        super().__init__(pontos)
        self.cor = cor
        self.width = width

        TrianguloGr._id += 1
        self.id = f"triang_{TrianguloGr._id}"

        self.tag = None

    def desenhaTriangulo(self, canvas):
        # RetaGr(self.pontos[0], self.pontos[1], self.cor, self.width).desenhaReta(canvas)
        # RetaGr(self.pontos[1], self.pontos[2], self.cor, self.width).desenhaReta(canvas)
        # RetaGr(self.pontos[2], self.pontos[0], self.cor, self.width).desenhaReta(canvas)

        for i, j in zip((0, 1, 2), (1, 2, 0)):
            RetaGr(self.pontos[i], self.pontos[j], self.cor, self.width).desenhaReta(canvas)

    def apagar(self, canvas):
        for p in self.pontos:
            p.cor = '#FFFFFF'
        self.desenhaTriangulo(canvas)

    def __del__(self):
        TrianguloGr._id -= 1

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='trg' + self.id[7:], bg='white')

            self.tag.place(x=self.pontos[2].x + self.width + 5, y=self.pontos[2].y + self.width + 3)
        else:
            if self.tag:
                self.tag.place_forget()


class CirculoGr(Circulo):
    _id = 0

    def __init__(self, centro, raio, cor, width=None):
        super().__init__(centro, raio)
        self.cor = cor
        self.width = width

        CirculoGr._id += 1
        self.id = f"circ_{CirculoGr._id}"

        self.tag = None

    def desenhaCircunferencia(self, canvas):
        angulo = 0
        while angulo <= 360:
            x = self.centro.x + self.raio * math.cos(math.radians(angulo))
            y = self.centro.y + self.raio * math.sin(math.radians(angulo))
            PontoGr(x, y, self.cor, self.width).desenhaPonto(canvas)
            angulo += 0.1

    def apagar(self, canvas):
        self.cor = '#FFFFFF'
        self.desenhaCircunferencia(canvas)

    def __del__(self):
        CirculoGr._id -= 1

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='c' + self.id[5:], bg='white')

            self.tag.place(x=self.centro.x, y=self.centro.y)
        else:
            if self.tag:
                self.tag.place_forget()


class Mandala:
    _id = 0
    tipo = 'mandala'

    def __init__(self, centro, raio, corCirc, corRetas, width):
        self.centro = centro
        self.raio = raio
        self.corCirc = corCirc
        self.corRetas = corRetas
        self.width = width

        Mandala._id += 1
        self.id = f"mand_{Mandala._id}"

        self.tag = None

    def desenhaMandala(self, canvas):
        # CIRCULOS

        # central
        c1 = CirculoGr(self.centro, self.raio, self.corCirc, self.width)
        c1.desenhaCircunferencia(canvas)

        altura_triang = (math.sqrt(3) * c1.raio) / 2

        # direito
        CirculoGr(PontoGr(c1.centro.x + c1.raio, c1.centro.y),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)
        # esquerdo
        CirculoGr(PontoGr(c1.centro.x - c1.raio, c1.centro.y),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)

        # diagonal superior direita
        CirculoGr(PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y - altura_triang),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)

        # diagonal superior esquerda
        CirculoGr(PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y - altura_triang),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)

        # diagonal inferior direita
        CirculoGr(PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y + altura_triang),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)

        # diagonal inferior esquerda
        CirculoGr(PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y + altura_triang),
                  self.raio, self.corCirc, self.width).desenhaCircunferencia(canvas)

        # RETÂNGULO

        RetanguloGr(PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                            self.corRetas, self.width),
                    PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                            self.corRetas, self.width),
                    self.corRetas, self.width).desenhaRetangulo(canvas)

        # RETAS

        # diagonal crescente do retângulo
        RetaGr(PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # diagonal decrescente do retângulo
        RetaGr(PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # reta vertical central
        RetaGr(PontoGr(c1.centro.x, c1.centro.y - 2 * altura_triang,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # reta horizontal central
        RetaGr(PontoGr(c1.centro.x - c1.raio, c1.centro.y,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x + c1.raio, c1.centro.y,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # diagonal decrescente do hexagono central
        RetaGr(PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y - altura_triang,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y + altura_triang,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # diagonal crescente do hexagono central
        RetaGr(PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y - altura_triang,
                       self.corRetas, self.width),
               PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y + altura_triang,
                       self.corRetas, self.width),
               self.corRetas, self.width).desenhaReta(canvas)

        # TRIÂNGULOS

        # triângulo central crescente
        TrianguloGr([PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x, c1.centro.y - 2 * altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                             self.corRetas, self.width)],
                    self.corRetas, self.width).desenhaTriangulo(canvas)

        # triângulo central decrescente
        TrianguloGr([PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.corRetas, self.width)],
                    self.corRetas, self.width).desenhaTriangulo(canvas)

        # triângulo superior
        TrianguloGr([PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x, c1.centro.y - 2 * altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.corRetas, self.width)],
                    self.corRetas, self.width).desenhaTriangulo(canvas)

        # triângulo inferior
        TrianguloGr([PontoGr(c1.centro.x - 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                             self.corRetas, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                             self.corRetas, self.width)],
                    self.corRetas, self.width).desenhaTriangulo(canvas)

    def apagar(self, canvas):
        self.corRetas = '#FFFFFF'
        self.corCirc = '#FFFFFF'

        self.desenhaMandala(canvas)

    def __del__(self):
        Mandala._id -= 1

    def exibe_tag(self, meu_canvas, flag):
        if flag:
            if self.tag is None:
                self.tag = Label(meu_canvas, text='m' + self.id[5:], bg='white')

            self.tag.place(x=self.centro.x + self.raio - self.width, y=self.centro.y + self.raio + self.width + 15)
        else:
            if self.tag:
                self.tag.place_forget()
