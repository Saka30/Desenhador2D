import customtkinter as ctk
from json_utils import JsonHandler
from primitivos import Ponto
from primitivos.graficos import TrianguloGr
from tkinter import Listbox, END, Canvas, Menu, filedialog


class DrawTools(ctk.CTkFrame):
    def __init__(self, container, tipo_primitivo, meu_canvas, espessura, width=120):
        super().__init__(container, width, fg_color='grey20')
        self.pack(side='left', fill='y')

        self.container = container
        self.tipo_primitivo = tipo_primitivo
        self.espessura = espessura
        self.meu_canvas = meu_canvas
        self.menuDeleta = None
        self.check_var = meu_canvas.check_var

        # Componentes
        BotaoArquivo(self)
        BotaoTipoDePrimitivo(self, self.modo_mandala, self.tipo_primitivo)
        ControleDeEspessura(self, self.espessura)
        EspessuraLabel(self, self.espessura)
        self.bc1 = BotaoCor(self, meu_canvas.cor, "cor")
        self.bc1.place(x=round(4.4 / 100 * container.largura), y=round(18 / 100 * container.altura))
        self.bc2 = BotaoCor(self, meu_canvas.mandala_cor2, "mandala_cor2")
        ctk.CTkLabel(self, text='Escolher Cor'
                     ).place(x=round(2.5 / 100 * container.largura), y=round(0.24 * container.altura))
        ctk.CTkCheckBox(self, text='Mostrar tags', command=self.mostrar_tags,
                        variable=self.check_var, onvalue="on", offvalue="off"
                        ).place(x=round(1 / 100 * container.largura), y=round(0.75 * container.altura))
        BotaoRedesenhar(self, self.meu_canvas)
        BotaoExclui(self, self.meu_canvas)

    def callMenuDeleta(self):
        if self.menuDeleta is None or not self.menuDeleta.winfo_exists():
            self.menuDeleta = MenuDeleta(self.container, self.meu_canvas)
            self.menuDeleta.attributes("-topmost", True)
            self.menuDeleta.protocol("WM_DELETE_WINDOW", self.menuDeleta.close_window)
        else:
            self.menuDeleta.focus()

    def modo_mandala(self, option):
        if option == "mandala":
            self.bc1.place(x=round(1.5 / 100 * self.container.largura),
                           y=round(18 / 100 * self.container.altura))
            self.bc2.place(x=round(7 / 100 * self.container.largura),
                           y=round(18 / 100 * self.container.altura))
            self.bc1.nome_atributo = "mandala_cor1"
            self.bc1.configure(bg=self.meu_canvas.mandala_cor1)
        else:
            self.bc2.place_forget()
            self.bc1.place(x=round(4.4 / 100 * self.container.largura),
                           y=round(18 / 100 * self.container.altura))
            self.bc1.nome_atributo = "cor"
            self.bc1.configure(bg=self.meu_canvas.cor)

    def mostrar_tags(self):
        flag = True if self.check_var.get() == "on" else False
        primitivos = self.meu_canvas.lista_primitivos
        for i in range(len(primitivos)):
            primitivos[i].exibe_tag(self.meu_canvas, flag)


class BotaoArquivo(ctk.CTkLabel):
    def __init__(self, container):
        super().__init__(container, text="Arquivo", bg_color='white', fg_color='#121212',
                         width=120, height=30, font=('San Francisco', 13), pady=8)
        self.place(x=0, y=0)

        self.arquivo_selecionado = None
        self.meu_canvas = container.meu_canvas
        self.container = container.container

        self.fileMenu = Menu(self, tearoff=0)
        self.fileMenu.add_command(label="Abrir", command=self.abrirArquivo)
        self.fileMenu.add_command(label='Salvar', command=self.salvarArquivo)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Sair", command=container.quit)

        self.bind("<Enter>", self.selecionado)
        self.bind("<Leave>", self.desselecionado)
        self.bind("<Button-1>", self.callMenu)

    def callMenu(self, event):
        self.fileMenu.post(event.x_root, event.y_root)

    def abrirArquivo(self):
        path = filedialog.askopenfilename(initialdir='Downloads',
                                          title='Selecionar arquivo',
                                          filetypes=(("json files", '*.json'),))
        if path:
            with open(path, 'r') as file_json:
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

    def selecionado(self, event):
        self.configure(fg_color='#646464')

    def desselecionado(self, event):
        self.configure(fg_color='#121212')


class BotaoTipoDePrimitivo(ctk.CTkOptionMenu):
    def __init__(self, container, comando, tipo_primitvo):
        super().__init__(master=container,
                         values=['ponto', 'reta', 'triângulo', 'retângulo', 'circulo', 'mandala'],
                         width=115,
                         variable=tipo_primitvo,
                         command=comando)
        self.app = container.container

        self.place(x=round((0.2 / 100) * self.app.largura), y=round((9 / 100) * self.app.altura))
        self.set('Figura')


class BotaoExclui(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Excluir'):
        super().__init__(container, text=texto, command=container.callMenuDeleta, width=80)
        self.app = container.container

        self.place(x=round((1.5 / 100) * self.app.largura), y=round(0.93 * self.app.altura))


class BotaoRedesenhar(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Redesenhar'):
        super().__init__(container, text=texto, command=meu_canvas.redesenhar, width=80)
        self.app = container.container

        self.place(x=round((1.5 / 100) * self.app.largura), y=round(0.85 * self.app.altura))


class BotaoCor(Canvas):
    def __init__(self, container, cor, nome_atributo):
        self.cor = cor
        self.nome_atributo = nome_atributo
        self.meu_canvas = container.meu_canvas
        self.app = container.container

        super().__init__(container, height=round(2 / 100 * self.app.largura),
                         width=round(3.5 / 100 * self.app.altura), relief='sunken',
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
        self.app = container.container

        self.place(x=round((4.7 / 100) * self.app.largura), y=round(0.3 * self.app.altura))


class EspessuraLabel(ctk.CTkLabel):
    def __init__(self, container, espessura):
        super().__init__(container, textvariable=espessura, text_color='white')
        self.app = container.container
        x, y = round((1.75 / 100) * self.app.largura), round(0.66 * self.app.altura)

        ctk.CTkLabel(container, text='Espessura: ').place(x=x, y=y)
        self.place(x=x + 70, y=y)


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
            self.warning.place_forget()

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
        self.warning.place(x=5, y=self.meu_canvas.altura * 0.95)


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

        ctk.CTkButton(self, text='Rotacionar', command=self.aguarda_ponto, width=80).pack(side='bottom')

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

        # trg = TrianguloGr(self.primitivo_selecionado.pontos, cor=self.primitivo_selecionado.cor,
        #             width=self.primitivo_selecionado.width)

        # for i in range(35):
        #     novo_trg = trg.rotaciona(self.angulo, Ponto(event.x, event.y))
        #     novo_trg.cor = choice(["#ff0000","#00ff00",'#0000ff', "#ffff00", "#8A2BE2", "#7FFFD4", 
        #     '#FF1493', '#FF7F50', '#E0FFFF', '#D2691E'])
        #     self.meu_canvas.lista_primitivos.append(novo_trg)

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

        ctk.CTkEntry(self, textvariable=self.sx).place(x=50, y=170)
        ctk.CTkEntry(self, placeholder_text="Sy: ", textvariable=self.sy).place(x=200, y=170)

        ctk.CTkButton(self, text='Escalar', command=self.aguarda_ponto, width=80).pack(side='bottom')

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
