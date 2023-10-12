import math


class Ponto:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, numero):
        return Ponto(self.x + numero, self.y + numero)

    def __sub__(self, outro):
        # retorna a distancia entre os dois pontos
        if isinstance(outro, Ponto):
            d = math.sqrt((self.y - outro.y) ** 2 + (self.x - outro.x) ** 2)
            return d
        return Ponto(self.x - outro, self.y - outro)


    def copiar(self):
        return Ponto(self.x, self.y)

    def __eq__(self, outro_ponto):
        is_equal = False
        if isinstance(outro_ponto, Ponto):
            if self.x == outro_ponto.x and self.y == outro_ponto.y:
                is_equal = True
        return is_equal

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f'Ponto({self.x}, {self.y})'


class Reta:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __equal__(self, outra_reta):
        return self.p1 == outra_reta.p1 and self.p2 == outra_reta.p2

    def calcularM(self):
        m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

        return m

    def calcularB(self):
        b = self.p1.y - self.calcularM() * self.p1.x

        return b

    def __str__(self):
        s = f'P1{self.p1} P2{self.p2}\nEq. da reta: y = {self.calcularM()}*x + {self.calcularB()}'

        return s


class Retangulo:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Triangulo:
    def __init__(self, pontos):
        self.pontos = pontos

class Circulo:
    def __init__(self, centro=Ponto(0,0), raio=0):
        self.centro = centro
        self.raio = raio

    def calcular_cincurferencia(self):
        return 2 * math.pi * self.raio

    def calcular_area(self):
        return math.pi * self.raio ** 2


