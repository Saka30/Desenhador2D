import math

from primitivos import *


class PontoGr(Ponto):
    def __init__(self, x=0, y=0, cor='#000000', width=None):
        super().__init__(x, y)
        self.width = width
        self.cor = cor

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
        raio = self.width.get()
        canvas.create_oval(
            (self.x - raio, self.y - raio),
            (self.x + raio, self.y + raio),
            fill=self.cor, outline=self.cor)


class RetaGr(Reta):

    def desenhaReta(self, canvas):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        steps = round(1 if steps == 0 else steps)

        incremento_x = dx / float(steps)
        incremento_y = dy / float(steps)

        ponto_inicial = self.p1.copiar()
        for v in range(0, steps):
            ponto_inicial.x += incremento_x
            ponto_inicial.y += incremento_y
            ponto_inicial.desenhaPonto(canvas)


class RetanguloGr(Retangulo):

    def __init__(self, p1, p2, width):
        super().__init__(p1, p2)
        self.width = width

    def desenhaRetangulo(self, canvas):
        cor = self.p1.cor
        RetaGr(self.p1, PontoGr(self.p1.x, self.p2.y, cor, self.width)).desenhaReta(canvas)
        RetaGr(PontoGr(self.p1.x, self.p2.y, cor, self.width), self.p2).desenhaReta(canvas)
        RetaGr(self.p2, PontoGr(self.p2.x, self.p1.y, cor, self.width)).desenhaReta(canvas)
        RetaGr(PontoGr(self.p2.x, self.p1.y, cor, self.width),
               PontoGr(self.p1.x, self.p1.y, cor, self.width)).desenhaReta(canvas)


class TrianguloGr(Triangulo):
    def desenhaTriangulo(self, canvas):
        RetaGr(self.pontos[0], self.pontos[1]).desenhaReta(canvas)
        RetaGr(self.pontos[1], self.pontos[2]).desenhaReta(canvas)
        RetaGr(self.pontos[2], self.pontos[0]).desenhaReta(canvas)


class CirculoGr(Circulo):
    def __init__(self, centro, raio, width=None):
        super().__init__(centro, raio)
        self.width = width

    def desenhaCircunferencia(self, canvas):
        angulo = 0
        while angulo <= 360:
            x = self.centro.x + self.raio * math.cos(math.radians(angulo))
            y = self.centro.y + self.raio * math.sin(math.radians(angulo))
            PontoGr(x, y, self.centro.cor, self.width).desenhaPonto(canvas)
            angulo += 0.1


class Mandala:
    def __init__(self, centro, raio, cor1, cor2, width):
        self.centro = centro
        self.raio = raio
        self.cor1 = cor1
        self.cor2 = cor2
        self.width = width

    def desenhaMandala(self, canvas):
        # CIRCULOS

        # central
        c1 = CirculoGr(self.centro, self.raio, self.width)
        c1.desenhaCircunferencia(canvas)

        altura_triang = (math.sqrt(3) * c1.raio) / 2

        # direito
        CirculoGr(PontoGr(c1.centro.x + c1.raio, c1.centro.y),
                  self.raio, self.width).desenhaCircunferencia(canvas)
        # esquerdo
        CirculoGr(PontoGr(c1.centro.x - c1.raio, c1.centro.y),
                  self.raio, self.width).desenhaCircunferencia(canvas)

        # diagonal superior direita
        CirculoGr(PontoGr(c1.centro.x + c1.raio/2, c1.centro.y - altura_triang),
                  self.raio, self.width).desenhaCircunferencia(canvas)

        # diagonal superior esquerda
        CirculoGr(PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y - altura_triang),
                  self.raio, self.width).desenhaCircunferencia(canvas)

        # diagonal inferior direita
        CirculoGr(PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y + altura_triang),
                  self.raio, self.width).desenhaCircunferencia(canvas)

        #diagonal inferior esquerda
        CirculoGr(PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y + altura_triang),
                  self.raio, self.width).desenhaCircunferencia(canvas)

        # RETÂNGULO

        RetanguloGr(PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y + altura_triang,
                            self.cor1, self.width),
                    PontoGr(c1.centro.x + 3*(c1.raio/2), c1.centro.y - altura_triang,
                            self.cor1, self.width),
                    self.width).desenhaRetangulo(canvas)

        # RETAS

        # diagonal crescente do retângulo
        RetaGr(PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y + altura_triang,
                            self.cor1, self.width),
               PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        # diagonal decrescente do retângulo
        RetaGr(PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y - altura_triang,
                       self.cor1, self.width),
               PontoGr(c1.centro.x + 3*(c1.raio/2), c1.centro.y + altura_triang,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        # reta vertical central
        RetaGr(PontoGr(c1.centro.x, c1.centro.y - 2 * altura_triang,
                             self.cor1, self.width),
               PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        # reta horizontal central
        RetaGr(PontoGr(c1.centro.x - c1.raio, c1.centro.y,
                       self.cor1, self.width),
               PontoGr(c1.centro.x + c1.raio, c1.centro.y,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        #diagonal decrescente do hexagono central
        RetaGr(PontoGr(c1.centro.x - c1.raio/2, c1.centro.y - altura_triang,
                       self.cor1, self.width),
               PontoGr(c1.centro.x + c1.raio/2, c1.centro.y + altura_triang,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        # diagonal crescente do hexagono central
        RetaGr(PontoGr(c1.centro.x + c1.raio / 2, c1.centro.y - altura_triang,
                       self.cor1, self.width),
               PontoGr(c1.centro.x - c1.raio / 2, c1.centro.y + altura_triang,
                       self.cor1, self.width)
               ).desenhaReta(canvas)

        # TRIÂNGULOS

        # triângulo central crescente
        TrianguloGr([PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y + altura_triang,
                            self.cor1, self.width),
                     PontoGr(c1.centro.x, c1.centro.y - 2*altura_triang,
                             self.cor1, self.width),
                     PontoGr(c1.centro.x + 3*(c1.raio/2), c1.centro.y + altura_triang,
                       self.cor1, self.width)]
                    ).desenhaTriangulo(canvas)

        # triângulo central decrescente
        TrianguloGr([PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y - altura_triang,
                       self.cor1, self.width),
                     PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                             self.cor1, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.cor1, self.width)
                     ]).desenhaTriangulo(canvas)

        # triângulo superior
        TrianguloGr([PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y - altura_triang,
                       self.cor1, self.width),
                     PontoGr(c1.centro.x, c1.centro.y - 2 * altura_triang,
                             self.cor1, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y - altura_triang,
                             self.cor1, self.width)
                     ]).desenhaTriangulo(canvas)

        # triângulo inferior
        TrianguloGr([PontoGr(c1.centro.x - 3*(c1.raio/2), c1.centro.y + altura_triang,
                            self.cor1, self.width),
                     PontoGr(c1.centro.x, c1.centro.y + 2 * altura_triang,
                             self.cor1, self.width),
                     PontoGr(c1.centro.x + 3 * (c1.raio / 2), c1.centro.y + altura_triang,
                             self.cor1, self.width)
                     ]).desenhaTriangulo(canvas)
