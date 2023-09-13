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
        self.espessura = espessura
        self.tipo_primitivo = tipo_primitivo
        self.coordenadas_var = ctk.StringVar(value='')

        # armazenadores de primitivos
        self.lista_pontos = LinkedList()
        self.lista_retas = LinkedList()
        self.lista_retangulos = LinkedList()
        self.lista_triangulos = LinkedList()
        self.lista_circulos = LinkedList()

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
                self.desenhaPonto(ponto_do_mouse_atual)
            case 'reta':
                self.desenhaReta(self.ponto_mouse_anterior, ponto_do_mouse_atual)
            case 'retângulo':
                self.desenhaRetangulo(self.ponto_mouse_anterior, ponto_do_mouse_atual)

            case 'triângulo':
                self.pontosTriangulo.append(ponto_do_mouse_atual)
                if len(self.pontosTriangulo) == 3:
                    pontosTriangulo = self.pontosTriangulo.copy()
                    self.desenhaTriangulo(pontosTriangulo)
                    self.pontosTriangulo.clear()
            case 'circulo':
                self.desenhaCincunferencia(ponto_do_mouse_atual)
            case 'mandala':
                self.desenhaMandala(ponto_do_mouse_atual)

    def desenhaPonto(self, ponto):
        ponto.desenhaPonto(self)
        # armazena ponto
        self.lista_pontos.append(ponto)

    def desenhaReta(self, ponto1, ponto2):

        if ponto1 != Ponto(None, None):
            reta = RetaGr(ponto1, ponto2)
            reta.desenhaReta(self)
            # armazena reta
            self.lista_retas.append(reta)

            self.ponto_mouse_anterior = PontoGr(x=None, y=None, width=self.espessura)
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
        # armazena triangulo
        self.lista_triangulos.append(triang)

    def desenhaCincunferencia(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            raio = ponto - self.ponto_mouse_anterior
            circ = CirculoGr(self.ponto_mouse_anterior, raio, self.espessura)
            print(circ.centro, circ.raio)
            circ.desenhaCircunferencia(self)
            # armazena circulo
            self.lista_circulos.append(circ)

            self.ponto_mouse_anterior = Ponto(None, None)
        else:
            self.ponto_mouse_anterior = ponto


    def desenhaMandala(self, ponto):
         if self.ponto_mouse_anterior != Ponto(None, None):
            raio = ponto - self.ponto_mouse_anterior
            mand = Mandala(self.ponto_mouse_anterior, raio, '#000000', '#000000', self.espessura)
            mand.desenhaMandala(self)

            self.ponto_mouse_anterior = Ponto(None, None)
         else:
             self.ponto_mouse_anterior = ponto

    def pegaCor(self):
        _, self.cor, = colorchooser.askcolor()

    def redesenhar(self):
        for i in range(len(self.lista_pontos)):
            self.desenhaPonto(self.lista_pontos[i])
            #self.lista_pontos[i].desenhaPonto(self)
            print(self.lista_pontos[i])

        for i in range(len(self.lista_retas)):
            #self.desenhaReta(self.lista_retas[i].p1, self.lista_retas[i].p2)
            self.lista_retas[i].desenhaReta(self)

        for i in range(len(self.lista_retangulos)):
            #self.desenhaRetangulo(self.lista_retangulos[i].p1, self.lista_retangulos[i].p2)
            self.lista_retangulos[i].desenhaRetangulo(self)

        for i in range(len(self.lista_triangulos)):
            self.desenhaTriangulo(self.lista_triangulos[i].pontos)

        for i in range(len(self.lista_circulos)):
            self.lista_circulos[i].desenhaCircunferencia(self)

        

    def deletaTudo(self):
        self.delete('all')
