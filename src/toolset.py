import re
from pathlib import Path
import customtkinter as ctk
from json_utils import JsonHandler
from primitivos import Ponto
from primitivos.graficos import TrianguloGr
from tkinter import Listbox, END, Canvas, filedialog


class DrawTools(ctk.CTkTabview):
    def __init__(self, container, tipo_primitivo, meu_canvas, espessura):
        super().__init__(container, fg_color='grey20')
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        # tabs
        self.add('A')
        self.add('B')
        self.add('C')

        self.set('B')

        self.container = container
        self.tipo_primitivo = tipo_primitivo
        self.espessura = espessura
        self.meu_canvas = meu_canvas
        self.menuDeleta = None
        self.check_var = meu_canvas.check_var

        vars_frameB = (self.tipo_primitivo,
                       self.espessura,
                       self.meu_canvas,
                       self.check_var,
                       self.mostrar_tags,
                       self.callMenuDeleta)

        # Componentes
        FrameA(self.tab('A'), self.meu_canvas, self.container)
        FrameB(self.tab('B'), *vars_frameB)
        FrameC(self.tab('C'), self.meu_canvas)

    def callMenuDeleta(self):
        if self.menuDeleta is None or not self.menuDeleta.winfo_exists():
            self.menuDeleta = MenuDeleta(self.container, self.meu_canvas)
            self.menuDeleta.attributes("-topmost", True)
            self.menuDeleta.protocol("WM_DELETE_WINDOW", self.menuDeleta.close_window)
        else:
            self.menuDeleta.focus()

    def mostrar_tags(self):
        flag = True if self.check_var.get() == "on" else False
        primitivos = self.meu_canvas.lista_primitivos
        for i in range(len(primitivos)):
            primitivos[i].exibe_tag(self.meu_canvas, flag)


class FrameA(ctk.CTkFrame):
    def __init__(self, container, meu_canvas, main_window):
        super().__init__(master=container, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.main_window = main_window
        self.meu_canvas = meu_canvas

        ctk.CTkButton(self, text='Abrir Desenho', command=self.abrirArquivo).pack(pady=20)
        ctk.CTkButton(self, text='Salvar Desenho', command=self.salvarArquivo).pack(pady=10)

    def abrirArquivo(self):
        path = filedialog.askopenfilename(initialdir=Path(__file__).parents[1] / 'Desenhos',
                                          title='Selecionar arquivo',
                                          filetypes=(("json files", '*.json'),))
        if path:
            with open(path, 'r') as file_json:
                self.main_window.title(path.split("/")[-1].replace(".json", ""))
                self.meu_canvas.lista_primitivos.clear()
                jsonHandler = JsonHandler(self.meu_canvas)
                self.meu_canvas.lista_primitivos = jsonHandler.read(file_json)
                self.meu_canvas.deletaTudo()
                self.meu_canvas.redesenhar()

    def salvarArquivo(self):
        path = filedialog.asksaveasfilename(initialdir='Downloads',
                                            title='Salvar arquivo',
                                            filetypes=(("json files", '*.json'),))

        if path:
            if not path.endswith('.json'):
                path += '.json'
            jsonHandler = JsonHandler(self.meu_canvas)
            jsonHandler.write(path, self.meu_canvas.lista_primitivos)
            self.main_window.title(path.split("/")[-1].replace(".json", ""))


class FrameB(ctk.CTkFrame):
    def __init__(self, container, tipo_primitivo, espessura,
                 meu_canvas, check_var, mostrar_tags, callMenuDeleta):
        super().__init__(master=container, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.meu_canvas = meu_canvas

        BotaoTipoDePrimitivo(self, self.modo_mandala, tipo_primitivo)
        ControleDeEspessura(self, espessura)
        EspessuraLabel(self, espessura)
        self.bc1 = BotaoCor(self, meu_canvas.cor, "cor", meu_canvas)
        self.bc1.pack(side='top', expand=True)
        self.bc2 = BotaoCor(self, meu_canvas.mandala_cor2, "mandala_cor2", meu_canvas)
        self.labelCor = ctk.CTkLabel(self, text='Escolher Cor')
        self.labelCor.pack()
        self.mostra_tags = ctk.CTkCheckBox(self, text='Mostrar tags', command=mostrar_tags,
                                           variable=check_var, onvalue="on", offvalue="off")

        self.mostra_tags.pack(side='top', pady=20, expand=True)

        BotaoExclui(self, callMenuDeleta)

    def modo_mandala(self, option):
        if option == "mandala":
            self.labelCor.pack_forget()
            self.mostra_tags.pack_forget()
            self.bc2.pack(side='top')
            self.labelCor.pack()
            self.mostra_tags.pack(side='top', pady=20, expand=True)
            self.bc1.nome_atributo = "mandala_cor1"
            self.bc1.configure(bg=self.meu_canvas.mandala_cor1)
        else:
            self.bc2.pack_forget()
            self.bc1.pack(side='top', expand=True)
            self.bc1.nome_atributo = "cor"
            self.bc1.configure(bg=self.meu_canvas.cor)


class FrameC(ctk.CTkFrame):
    def __init__(self, container, meu_canvas):
        super().__init__(master=container, fg_color='transparent')
        self.pack(expand=True, fill='both')

        ctk.CTkButton(self, text='Rotacionar', command=meu_canvas.callMenuRot).pack(pady=20)
        ctk.CTkButton(self, text='Escala', command=meu_canvas.callMenuEscala).pack(pady=10)


class BotaoTipoDePrimitivo(ctk.CTkOptionMenu):
    def __init__(self, container, comando, tipo_primitvo):
        super().__init__(master=container,
                         values=['ponto', 'reta', 'triângulo', 'retângulo', 'circulo', 'mandala'],
                         variable=tipo_primitvo,
                         command=comando)

        self.pack(side='top', pady=20)
        self.set('Figura')


class BotaoExclui(ctk.CTkButton):
    def __init__(self, container, function, texto='Excluir'):
        super().__init__(container, text=texto, command=function)

        self.pack(side='bottom', pady=15)


class BotaoCor(Canvas):
    def __init__(self, container, cor, nome_atributo, meu_canvas):
        self.cor = cor
        self.nome_atributo = nome_atributo
        self.meu_canvas = meu_canvas

        super().__init__(container, height=20,
                         width=20, relief='sunken',
                         bd=2, bg=self.cor, highlightbackground='gray')

        self.bind("<Button-1>", lambda event: self.altera_cor(self.nome_atributo))

    def altera_cor(self, nome_atributo):
        self.meu_canvas.pegaCor(nome_atributo)
        self.configure(bg=getattr(self.meu_canvas, nome_atributo))


class ControleDeEspessura(ctk.CTkSlider):
    def __init__(self, container, espessura):
        super().__init__(container,
                         from_=1, to=30,
                         width=18,
                         variable=espessura,
                         number_of_steps=30,
                         orientation='vertical')

        self.pack()


class EspessuraLabel(ctk.CTkLabel):
    def __init__(self, container, espessura):
        super().__init__(container, textvariable=espessura, text_color='white')

        ctk.CTkLabel(container, text='Espessura: ').pack()
        self.pack()


class MenuDePrimitivos(ctk.CTkToplevel):
    def __init__(self, container, title, meu_canvas):
        super().__init__(container)
        self.primitivo_selecionado = None
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.meu_canvas = meu_canvas
        self.listaPrimitivos = meu_canvas.lista_primitivos
        self.container = container
        self.warning = None

        ctk.CTkLabel(self, text='Figuras', text_color='white', font=("Arial", 14)).pack()

        self.listaFiguras = Listbox(self, highlightthickness=0, bd=2, bg='#353535', fg='#ffffff')
        self.listaFiguras.configure(width=60, height=7)
        self.listaFiguras.pack()

        for i in range(len(self.listaPrimitivos)):
            self.listaPrimitivos[i].exibe_tag(self.meu_canvas, True)

    def close_window(self):
        for i in range(len(self.listaPrimitivos)):
            self.listaPrimitivos[i].exibe_tag(self.meu_canvas, False)

        self.container.drawtools.mostrar_tags()
        self.destroy()

        if self.warning:
            self.warning.pack_forget()

        self.meu_canvas.bind("<Button-1>", self.meu_canvas.desenhaPrimitivo)

    def aguarda_ponto(self):
        for index_selecionado in self.listaFiguras.curselection():
            while (not isinstance(self.listaPrimitivos[index_selecionado], TrianguloGr) and
                   index_selecionado < len(self.listaPrimitivos)):
                index_selecionado += 1

            self.primitivo_selecionado = self.listaPrimitivos[index_selecionado]

        self.withdraw()

        self.warning = ctk.CTkLabel(self.meu_canvas, text="Aguardando ponto...",
                                    font=ctk.CTkFont(family='Arial', size=14, weight='bold'),
                                    text_color='red')
        self.warning.pack(side='bottom', anchor='sw', padx=10)


class MenuDeleta(MenuDePrimitivos):
    def __init__(self, container, meu_canvas, title="Excluir Figuras"):
        super().__init__(container, title, meu_canvas)
        self.container = container

        for i in range(len(self.listaPrimitivos)):
            self.listaFiguras.insert(END, self.listaPrimitivos[i].id)

        ctk.CTkButton(self, text='Excluir', command=self.destroyPrimitivos, width=80).pack(side='bottom')

    def destroyPrimitivos(self):

        for index_selecionado in self.listaFiguras.curselection():
            primitivo_selecionado = self.listaPrimitivos[index_selecionado]
            primitivo_selecionado.exibe_tag(self.meu_canvas, False)
            self.listaPrimitivos.remove(primitivo_selecionado)
            self.listaFiguras.delete(index_selecionado)
            self.meu_canvas.deletaTudo()
            self.meu_canvas.redesenhar()


class MenuRot(MenuDePrimitivos):

    def __init__(self, container, meu_canvas, title="Rotacionar figuras"):
        super().__init__(container, title, meu_canvas)
        self.geometry("400x250")
        self.angulo = ctk.IntVar(value=0)
        self.func_id = None

        # componentes
        ctk.CTkSlider(self, width=360, height=10, variable=self.angulo,
                      from_=0, to=360, number_of_steps=360).place(x=20, y=170)
        ctk.CTkLabel(self, text='Angulo:').place(x=160, y=180)
        ctk.CTkLabel(self, textvariable=self.angulo).place(x=210, y=180)
        ctk.CTkLabel(self, text='º').place(x=232, y=180)

        ctk.CTkButton(self, text='Rotacionar', command=self.aguarda_ponto, width=80).pack(side='bottom', pady=5)

        for i in range(len(self.listaPrimitivos)):
            primitivo = self.listaPrimitivos[i]
            if isinstance(primitivo, TrianguloGr):
                self.listaFiguras.insert(END, primitivo.id)

    def aguarda_ponto(self):
        super().aguarda_ponto()

        if self.primitivo_selecionado:
            self.meu_canvas.bind("<Button-1>", self.rotaciona)
        else:
            self.close_window()

    def rotaciona(self, event):
        self.primitivo_selecionado.rotaciona(self.angulo, Ponto(event.x, event.y))
        self.meu_canvas.deletaTudo()
        self.meu_canvas.redesenhar()
        self.close_window()


class MenuEscala(MenuDePrimitivos):
    def __init__(self, container, meu_canvas, title="Escala em relação a um ponto"):
        super().__init__(container, title, meu_canvas)
        self.geometry("400x250")

        self.sx = ctk.StringVar()
        self.sy = ctk.StringVar()

        for i in range(len(self.listaPrimitivos)):
            primitivo = self.listaPrimitivos[i]
            if isinstance(primitivo, TrianguloGr):
                self.listaFiguras.insert(END, primitivo.id)

        self.sx_entry = ctk.CTkEntry(self, textvariable=self.sx)
        self.sx_entry.place(x=50, y=170)

        self.sy_entry = ctk.CTkEntry(self, textvariable=self.sy)
        self.sy_entry.place(x=200, y=170)

        ctk.CTkButton(self, text='Aplicar', command=self.valida_entrada, width=80).pack(side='bottom', pady=10)

    def valida_entrada(self):
        soma = 0
        d = {self.sx.get(): self.sx_entry, self.sy.get(): self.sy_entry}
        for var in (self.sx.get(), self.sy.get()):
            if re.fullmatch(r'[+-]?\d+(\.\d+)?', var):
                soma += 1
                d[var].configure(border_color='gray')
            else:
                d[var].configure(border_color='red')

        if soma == 2:
            self.aguarda_ponto()

    def aguarda_ponto(self):
        super().aguarda_ponto()

        if self.primitivo_selecionado:
            self.meu_canvas.bind("<Button-1>", self.escala)
        else:
            self.close_window()

    def escala(self, event):
        self.primitivo_selecionado.escala(self.sx, self.sy, Ponto(event.x, event.y))
        self.meu_canvas.deletaTudo()
        self.meu_canvas.redesenhar()

        self.close_window()
