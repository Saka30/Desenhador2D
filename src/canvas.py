import customtkinter as ctk
from tkinter import Canvas, colorchooser, Menu
from primitivos.graficos import *
from linked_list import LinkedList
from toolset import MenuRot, MenuEscala


class AreaDeDesenho(Canvas):
    def __init__(self, container, espessura, tipo_primitivo):
        # setup
        super().__init__(container,
                         bg='white',
                         highlightthickness=0)

        self.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.configure(cursor='tcross')
       
        self.update()
        self.largura, self.altura = self.winfo_width(), self.winfo_height()

        # dados
        self.pontosTriangulo = []
        self.cor = '#000000'
        self.mandala_cor1 = '#417E4D'
        self.mandala_cor2 = '#DD3B35'
        self.espessura = espessura
        self.tipo_primitivo = tipo_primitivo
        self.coordenadas_var = ctk.StringVar(value='0, 0px')
        self.check_var = ctk.StringVar(value="off")
        self.container = container
        self.menuRotaciona = None
        self.menuEscala = None

        # Armazenador de primitivos
        self.lista_primitivos = LinkedList()

        # cria um menu de opçoes
        self.subMenu = Menu(self, tearoff=0)
        self.subMenu.add_command(label="Limpa tudo", command=self.limpaTudo)
        self.subMenu.add_command(label="Rotacionar", command=self.callMenuRot)
        self.subMenu.add_command(label="Escala", command=self.callMenuEscala)
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Sair", command=container.quit)

        #coordenadas
        ctk.CTkLabel(self, text_color='black', textvariable=self.coordenadas_var,
                     font=ctk.CTkFont(family='Consolas', size=14)
                     ).pack(side='bottom', anchor='se', padx=10)

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

    def callMenuRot(self):
        if self.menuRotaciona is None or not self.menuRotaciona.winfo_exists():
            self.menuRotaciona = MenuRot(self.container, self)
            self.menuRotaciona.attributes("-topmost", True)
            self.menuRotaciona.protocol("WM_DELETE_WINDOW", self.menuRotaciona.close_window)
        else:
            self.menuRotaciona.focus()

    def callMenuEscala(self):
        if self.menuEscala is None or not self.menuEscala.winfo_exists():
            self.menuEscala = MenuEscala(self.container, self)
            self.menuEscala.attributes("-topmost", True)
            self.menuEscala.protocol("WM_DELETE_WINDOW", self.menuEscala.close_window)
        else:
            self.menuEscala.focus()

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
                primitivo = self.desenhaCincunferencia(self.ponto_mouse_anterior, ponto_do_mouse_atual)
            case 'mandala':
                primitivo = self.desenhaMandala(ponto_do_mouse_atual)

        if primitivo:
            self.lista_primitivos.append(primitivo)
            if self.check_var.get() == "on":
                primitivo.exibe_tag(self, True)

    def desenhaPonto(self, ponto):
        p = PontoGr(ponto.x, ponto.y, self.cor, self.espessura.get())
        p.desenha(self)

        return p
    
    def desenhaForma(self, ponto1, ponto2, classe):
        if ponto1 != Ponto(None, None):

            if classe is CirculoGr:
                raio = ponto2 - ponto1
                ponto2 = raio

            forma = classe(ponto1, ponto2, self.cor, self.espessura.get())
            self.ponto_mouse_anterior = Ponto(x=None, y=None)

            return forma
        else:
            self.ponto_mouse_anterior = ponto2

    def desenhaReta(self, ponto1, ponto2):
        reta = self.desenhaForma(ponto1, ponto2, RetaGr)
        if reta:
            reta.desenha(self)
            return reta
    
    def desenhaRetangulo(self, ponto1, ponto2):
        retang = self.desenhaForma(ponto1, ponto2, RetanguloGr)
        if retang:
            retang.desenha(self)
            return retang

    def desenhaTriangulo(self, pontos):
        triang = TrianguloGr(pontos, self.cor, self.espessura.get())
        triang.desenha(self)

        return triang

    def desenhaCincunferencia(self, ponto1, ponto2):
        circ = self.desenhaForma(ponto1, ponto2, CirculoGr)
        if circ:
            circ.desenha(self)
            return circ

    def desenhaMandala(self, ponto):
        if self.ponto_mouse_anterior != Ponto(None, None):
            mand = Mandala(self.ponto_mouse_anterior, ponto, self.mandala_cor1,
                           self.mandala_cor2, self.espessura.get())
            mand.desenha(self)

            self.ponto_mouse_anterior = Ponto(None, None)
            return mand
        else:
            self.ponto_mouse_anterior = ponto

    def pegaCor(self, nome_atributo):
        setattr(self, nome_atributo, colorchooser.askcolor()[1])

    def redesenhar(self):
        for i in range(len(self.lista_primitivos)):
            primitivo = self.lista_primitivos[i]
            primitivo.desenha(self)

    def limpaTudo(self, event=None):
        for i in range(len(self.lista_primitivos)):
            self.lista_primitivos[i].exibe_tag(self, False)

        self.lista_primitivos.clear()
        self.deletaTudo()

    def deletaTudo(self, event=None):
        self.delete('all')
