import customtkinter as ctk
from tkinter import Canvas, colorchooser, Menu
from primitivos.graficos import *
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
        self.check_var = ctk.StringVar(value="off")

        # Armazenador de primitivos
        self.lista_primitivos = LinkedList()

        # cria um menu de opçoes
        self.subMenu = Menu(self, tearoff=0)
        self.subMenu.add_command(label="Limpar memória", command=self.limpaMemoria)
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Sair", command=container.quit)

        self.coordenadas = ctk.CTkLabel(self,
                                        text_color='black',
                                        textvariable=self.coordenadas_var,
                                        font=ctk.CTkFont(family='Consolas', size=14)).place(x=590, y=575)

        # start_point
        self.ponto_mouse_anterior = Ponto(x=None, y=None)

        # input
        self.bind("<Button-1>", self.desenhaPrimitivo)
        self.bind("<Button-3>", self.callSubMenu)
        self.bind("<Motion>", self.changeCoordinates)

    def changeCoordinates(self, event):
        self.coordenadas_var.set(value=f'{event.x}, {event.y}px')

    def callSubMenu(self, event):
        self.subMenu.post(event.x_root, event.y_root)

    def desfaz(self, event):
        if not self.lista_primitivos.is_empty():
            p = self.lista_primitivos.pop()
            p.exibe_tag(self, False)
            self.deletaTudo()
            self.redesenhar()

    def desenhaPrimitivo(self, event):
        ponto_do_mouse_atual = Ponto(event.x, event.y)
        primitivo = None
        match self.tipo_primitivo.get():
            case 'ponto':
                primitivo = self.desenhaPonto(ponto_do_mouse_atual)
            case 'reta':
                primitivo = self.desenhaReta(self.ponto_mouse_anterior, ponto_do_mouse_atual)
            case 'retângulo':
                primitivo = self.desenhaRetangulo(self.ponto_mouse_anterior, ponto_do_mouse_atual)
            case 'triângulo':
                self.pontosTriangulo.append(ponto_do_mouse_atual)
                if len(self.pontosTriangulo) == 3:
                    pontosTriangulo = self.pontosTriangulo.copy()
                    primitivo = self.desenhaTriangulo(pontosTriangulo)
                    self.pontosTriangulo.clear()
            case 'circulo':
                primitivo = self.desenhaCincunferencia(ponto_do_mouse_atual)
            case 'mandala':
                primitivo = self.desenhaMandala(ponto_do_mouse_atual)

        if primitivo is not None:
            self.lista_primitivos.append(primitivo)
            if self.check_var.get() == "on":
                primitivo.exibe_tag(self, True)

    def desenhaPonto(self, ponto):
        p = PontoGr(ponto.x, ponto.y, self.cor, self.espessura.get())
        p.desenhaPonto(self)

        return p

    def desenhaReta(self, ponto1, ponto2):

        if ponto1 != Ponto(None, None):
            reta = RetaGr(ponto1, ponto2, self.cor, self.espessura.get())
            reta.desenhaReta(self)
            self.ponto_mouse_anterior = Ponto(x=None, y=None)

            return reta
        else:
            self.ponto_mouse_anterior = ponto2

    def desenhaRetangulo(self, ponto1, ponto2):

        if ponto1 != Ponto(None, None):
            retang = RetanguloGr(ponto1, ponto2, self.cor, self.espessura.get())
            retang.desenhaRetangulo(self)

            self.ponto_mouse_anterior = Ponto(x=None, y=None)

            return retang
        else:
            self.ponto_mouse_anterior = ponto2

    def desenhaTriangulo(self, pontos):
        triang = TrianguloGr(pontos, self.cor, self.espessura.get())
        triang.desenhaTriangulo(self)

        return triang

    def desenhaCincunferencia(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            raio = ponto - self.ponto_mouse_anterior
            circ = CirculoGr(self.ponto_mouse_anterior, raio, self.cor, self.espessura.get())
            circ.desenhaCircunferencia(self)

            self.ponto_mouse_anterior = Ponto(None, None)
            return circ
        else:
            self.ponto_mouse_anterior = ponto

    def desenhaMandala(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            mand = Mandala(self.ponto_mouse_anterior, ponto, self.mandala_cor1,
                           self.mandala_cor2, self.espessura.get())
            mand.desenhaMandala(self)

            self.ponto_mouse_anterior = Ponto(None, None)
            return mand
        else:
            self.ponto_mouse_anterior = ponto

    def pegaCor(self, nome_atributo):
        setattr(self, nome_atributo, colorchooser.askcolor()[1])

    def redesenhar(self):
        for i in range(len(self.lista_primitivos)):
            primitivo = self.lista_primitivos[i]
            match primitivo:
                case PontoGr():
                    primitivo.desenhaPonto(self)
                case RetaGr():
                    primitivo.desenhaReta(self)
                case TrianguloGr():
                    primitivo.desenhaTriangulo(self)
                case RetanguloGr():
                    primitivo.desenhaRetangulo(self)
                case CirculoGr():
                    primitivo.desenhaCircunferencia(self)
                case Mandala():
                    primitivo.desenhaMandala(self)

    def limpaMemoria(self):
        self.lista_primitivos.clear()

    def deletaTudo(self, event=None):
        self.delete('all')
