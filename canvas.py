import customtkinter as ctk
from tkinter import Canvas
from primitivos.graficos import *
from tkinter import colorchooser
from linked_list import LinkedList


class AreaDeDesenho(Canvas):
    def __init__(self, container, espessura, tipo_primitivo):
        # setup
        super().__init__(container,
                         bg='white',
                         highlightthickness=0)

        self.pack(side='right', fill='both', expand=True)
        self.configure(cursor='tcross')

        # dados
        self.pontosTriangulo = []
        self.cor = '#000000'
        self.mandala_cor1 = '#417E4D'
        self.mandala_cor2 = '#DD3B35'
        self.espessura = espessura
        self.tipo_primitivo = tipo_primitivo
        self.coordenadas_var = ctk.StringVar(value='')

        # armazenadores de primitivos
        self.lista_pontos = LinkedList()
        self.lista_retas = LinkedList()
        self.lista_retangulos = LinkedList()
        self.lista_triangulos = LinkedList()
        self.lista_circulos = LinkedList()
        self.lista_mandalas = LinkedList()

        self.coordenadas = ctk.CTkLabel(self,
                                        text_color='black',
                                        textvariable=self.coordenadas_var,
                                        font=ctk.CTkFont(family='Consolas', size=14)).place(x=590, y=575)

        # start_point
        self.ponto_mouse_anterior = PontoGr(x=None, y=None, cor=self.cor, width=self.espessura)

        # input
        self.bind("<Button-1>", self.desenhaPrimitivo)
        self.bind('<Motion>', self.changeCoordinates)

    def changeCoordinates(self, event):
        self.coordenadas_var.set(value=f'{event.x}, {event.y}px')

    def desenhaPrimitivo(self, event):
        ponto_do_mouse_atual = PontoGr(event.x, event.y, self.cor, self.espessura)

        match self.tipo_primitivo.get():
            case 'ponto':
                p = self.desenhaPonto(ponto_do_mouse_atual)
                self.armazenar(p)
            case 'reta':
                r = self.desenhaReta(self.ponto_mouse_anterior, ponto_do_mouse_atual)
                self.armazenar(r)
            case 'retângulo':
                rtg = self.desenhaRetangulo(self.ponto_mouse_anterior, ponto_do_mouse_atual)
                self.armazenar(rtg)
            case 'triângulo':
                self.pontosTriangulo.append(ponto_do_mouse_atual)
                if len(self.pontosTriangulo) == 3:
                    pontosTriangulo = self.pontosTriangulo.copy()
                    trg = self.desenhaTriangulo(pontosTriangulo)
                    self.armazenar(trg)
                    self.pontosTriangulo.clear()
            case 'circulo':
                circ = self.desenhaCincunferencia(ponto_do_mouse_atual)
                self.armazenar(circ)
            case 'mandala':
                mand = self.desenhaMandala(ponto_do_mouse_atual)
                self.armazenar(mand)

    def armazenar(self, primitivo):
        match primitivo:
            case PontoGr():
                self.lista_pontos.append(primitivo)
            case RetaGr():
                self.lista_retas.append(primitivo)
            case RetanguloGr():
                self.lista_retangulos.append(primitivo)
            case TrianguloGr():
                self.lista_triangulos.append(primitivo)
            case CirculoGr():
                self.lista_circulos.append(primitivo)
            case Mandala():
                self.lista_mandalas.append(primitivo)

    def desenhaPonto(self, ponto):
        ponto.desenhaPonto(self)

        return ponto

    def desenhaReta(self, ponto1, ponto2):

        if ponto1 != Ponto(None, None):
            reta = RetaGr(ponto1, ponto2)
            reta.desenhaReta(self)
            self.ponto_mouse_anterior = PontoGr(x=None, y=None, width=self.espessura)

            return reta
        else:
            self.ponto_mouse_anterior = ponto2

    def desenhaRetangulo(self, ponto1, ponto2):

        if ponto1 != Ponto(None, None):
            retang = RetanguloGr(ponto1, ponto2, self.espessura)
            retang.desenhaRetangulo(self)
            # armazena retangulo
            self.lista_retangulos.append(retang)

            self.ponto_mouse_anterior = PontoGr(x=None, y=None, width=self.espessura)
        else:
            self.ponto_mouse_anterior = ponto2

    def desenhaTriangulo(self, pontos):
        triang = TrianguloGr(pontos)
        triang.desenhaTriangulo(self)

        return triang

    def desenhaCincunferencia(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            raio = ponto - self.ponto_mouse_anterior
            circ = CirculoGr(self.ponto_mouse_anterior, raio, self.cor, self.espessura)
            circ.desenhaCircunferencia(self)

            self.ponto_mouse_anterior = Ponto(None, None)
            return circ
        else:
            self.ponto_mouse_anterior = ponto

    def desenhaMandala(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            raio = ponto - self.ponto_mouse_anterior
            # mand = Mandala(self.ponto_mouse_anterior, raio, '#417E4D', '#DD3B35', self.espessura)
            mand = Mandala(self.ponto_mouse_anterior, raio, self.mandala_cor1, self.mandala_cor2, self.espessura)
            mand.desenhaMandala(self)

            self.ponto_mouse_anterior = Ponto(None, None)
            return mand
        else:
            self.ponto_mouse_anterior = ponto

    def pegaCor(self, nome_atributo):
        setattr(self, nome_atributo,  colorchooser.askcolor()[1])


    def redesenhar(self):
        for i in range(len(self.lista_pontos)):
            self.desenhaPonto(self.lista_pontos[i])

        for i in range(len(self.lista_retas)):
            self.lista_retas[i].desenhaReta(self)

        for i in range(len(self.lista_retangulos)):
            self.lista_retangulos[i].desenhaRetangulo(self)

        for i in range(len(self.lista_triangulos)):
            self.desenhaTriangulo(self.lista_triangulos[i].pontos)

        for i in range(len(self.lista_circulos)):
            self.lista_circulos[i].desenhaCircunferencia(self)

        for i in range(len(self.lista_mandalas)):
            self.lista_mandalas[i].desenhaMandala(self)

    def deletaTudo(self):
        self.delete('all')
