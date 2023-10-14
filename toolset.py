import customtkinter as ctk
from tkinter import Listbox, END


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
        BotaoTipoDePrimitivo(self, self.modo_mandala, self.tipo_primitivo)
        ControleDeEspessura(self, self.espessura)
        EspessuraLabel(self, self.espessura)
        self.bc1 = BotaoCor(self, lambda: self.meu_canvas.pegaCor("cor"))
        self.bc1.place(x=15, y=85)
        self.bc2 = BotaoCor(self, lambda: self.meu_canvas.pegaCor("mandala_cor2"), texto="Cor 2")
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
            self.bc2.place(x=15, y=135)
            self.bc1.configure(text="Cor 1")
            self.bc1.configure(command=lambda: self.meu_canvas.pegaCor("mandala_cor1"))
        else:
            self.bc2.place_forget()
            self.bc1.configure(text="Escolher Cor")
            self.bc1.configure(command=lambda: self.meu_canvas.pegaCor("cor"))

    def mostrar_tags(self):
        flag = True if self.check_var.get() == "on" else False
        primitivos = self.meu_canvas.lista_primitivos
        for i in range(len(primitivos)):
            primitivos[i].exibe_tag(self.meu_canvas, flag)


class BotaoTipoDePrimitivo(ctk.CTkOptionMenu):
    def __init__(self, container, comando, tipo_primitvo):
        super().__init__(master=container,
                         values=['ponto', 'reta', 'triângulo', 'retângulo', 'circulo', 'mandala'],
                         width=115,
                         variable=tipo_primitvo,
                         command=comando)

        self.place(x=2, y=25)
        self.set('Figura')


class BotaoExclui(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Excluir'):
        super().__init__(container, text=texto, command=container.callMenuDeleta, width=80)

        self.place(x=15, y=550)


class BotaoRedesenhar(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Redesenhar'):
        super().__init__(container, text=texto, command=meu_canvas.redesenhar, width=80)

        self.place(x=15, y=490)


class BotaoCor(ctk.CTkButton):
    def __init__(self, container, comando, texto='Escolher Cor', ):
        super().__init__(container, text=texto, command=comando, width=80)


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
