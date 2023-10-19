import customtkinter as ctk
from json_utils import JsonReader
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
        self.bc1.place(x=45, y=105)
        self.bc2 = BotaoCor(self, meu_canvas.mandala_cor2, "mandala_cor2")
        ctk.CTkLabel(self,text='Escolher Cor').place(x=25, y=140)
        ctk.CTkCheckBox(self, text='Mostrar tags', command=self.mostrar_tags,
                        variable=self.check_var, onvalue="on", offvalue="off").place(x=10, y=430)
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
            self.bc1.place(x=15, y=105)
            self.bc2.place(x=72, y=105)
            self.bc1.nome_atributo = "mandala_cor1"
            self.bc1.configure(bg = self.meu_canvas.mandala_cor1)
        else:
            self.bc2.place_forget()
            self.bc1.place(x=45, y=105)
            self.bc1.nome_atributo = "cor"
            self.bc1.configure(bg = self.meu_canvas.cor)

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

        self.fileMenu = Menu(self, tearoff=0)
        self.fileMenu.add_command(label="Abrir", command=self.abrirArquivo)
        self.fileMenu.add_command(label='Salvar')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Sair", command=container.quit)

        self.bind("<Enter>", self.selecionado)
        self.bind("<Leave>", self.desselecionado)
        self.bind("<Button-1>", self.callMenuSalvar)

    def callMenuSalvar(self, event):
        self.fileMenu.post(event.x_root, event.y_root)

    def abrirArquivo(self):
        self.arquivo_selecionado = filedialog.askopenfilename(initialdir='Downloads',
                                                              title='Selecionar arquivo',
                                                              filetypes=(("json files", '*.json'),))
        if self.arquivo_selecionado != '':
            with open(self.arquivo_selecionado) as file_json:
                self.meu_canvas.lista_primitivos.clear()
                self.meu_canvas.lista_primitivos = JsonReader.read(file_json)
                self.meu_canvas.deletaTudo()
                self.meu_canvas.redesenhar()

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

        self.place(x=2, y=50)
        self.set('Figura')


class BotaoExclui(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Excluir'):
        super().__init__(container, text=texto, command=container.callMenuDeleta, width=80)

        self.place(x=15, y=550)


class BotaoRedesenhar(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Redesenhar'):
        super().__init__(container, text=texto, command=meu_canvas.redesenhar, width=80)

        self.place(x=15, y=490)


class BotaoCor(Canvas):
    def __init__(self, container, cor, nome_atributo):
        self.cor = cor
        self.nome_atributo = nome_atributo
        self.meu_canvas = container.meu_canvas
        super().__init__(container, height=20, width=20, relief='sunken',
                         bd=2, bg = self.cor,  highlightbackground='gray')

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

        self.place(x=48, y=170)


class EspessuraLabel(ctk.CTkLabel):
    def __init__(self, container, espessura):
        super().__init__(container, textvariable=espessura, text_color='white')
        x, y = 18, 380

        ctk.CTkLabel(container, text='Espessura: ').place(x=x, y=y)
        self.place(x=x + 70, y=y)


class MenuDeleta(ctk.CTkToplevel):
    def __init__(self, container, meu_canvas):
        super().__init__(container)
        self.title("Excluir figuras")
        self.geometry("400x200")
        self.resizable(False, False)
        self.meu_canvas = meu_canvas
        self.listaPrimitivos = meu_canvas.lista_primitivos
        self.container = container

        ctk.CTkLabel(self, text='Figuras', text_color='white', font=("Arial", 14)).pack()

        self.listaFiguras = Listbox(self, highlightthickness=0, bd=2, bg='#353535', fg='#ffffff')
        self.listaFiguras.configure(width=60, height=7)
        self.listaFiguras.pack()

        for i in range(len(self.listaPrimitivos)):
            self.listaFiguras.insert(END, self.listaPrimitivos[i].id)

        ctk.CTkButton(self, text='Excluir', command=self.destroyPrimitivos, width=80).pack(side='bottom')

        for i in range(len(self.listaPrimitivos)):
            self.listaPrimitivos[i].exibe_tag(self.meu_canvas, True)

    def destroyPrimitivos(self):

        for index_selecionado in self.listaFiguras.curselection():
            primitivo_selecionado = self.listaPrimitivos[index_selecionado]
            primitivo_selecionado.exibe_tag(self.meu_canvas, False)
            self.listaPrimitivos.remove(primitivo_selecionado)
            self.listaFiguras.delete(index_selecionado)
            self.meu_canvas.deletaTudo()
            self.meu_canvas.redesenhar()

    def close_window(self):
        for i in range(len(self.listaPrimitivos)):
            self.listaPrimitivos[i].exibe_tag(self.meu_canvas, False)

        self.container.drawtools.mostrar_tags()
        self.destroy()
