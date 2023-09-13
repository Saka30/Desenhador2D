import customtkinter as ctk


class DrawTools(ctk.CTkFrame):
    def __init__(self, container, tipo_primitivo, meu_canvas, espessura, width=120):
        super().__init__(container, width, fg_color='grey20')
        self.pack(side='left', fill='y')

        self.tipo_primitivo = tipo_primitivo
        self.espessura = espessura

        # Componentes
        BotaoTipoDePrimitivo(self, self.tipo_primitivo)
        ControleDeEspessura(self, self.espessura)
        EspessuraLabel(self, self.espessura)
        BotaoCor(self, meu_canvas)
        BotaoRedesenhar(self, meu_canvas)
        BotaoLimpaTudo(self, meu_canvas)


class BotaoTipoDePrimitivo(ctk.CTkOptionMenu):
    def __init__(self, container, tipo_primitvo):
        super().__init__(master=container,
                         values=['ponto', 'reta', 'triângulo', 'retângulo', 'circulo', 'mandala'],
                         width=115,
                         variable=tipo_primitvo)

        self.place(x=2, y=40)
        self.set('Figura')

class BotaoLimpaTudo(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto = 'Limpar'):
        super().__init__(container, text=texto, command=meu_canvas.deletaTudo, width=80)

        self.place(x=15, y=540)

class BotaoRedesenhar(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Redesenhar'):
        super().__init__(container, text=texto, command=meu_canvas.redesenhar, width=80)

        self.place(x=15, y=470)

class BotaoCor(ctk.CTkButton):
    def __init__(self, container, meu_canvas, texto='Escolher Cor', ):
        super().__init__(container, text=texto, command=meu_canvas.pegaCor, width=80)

        self.place(x=15, y=110)


class ControleDeEspessura(ctk.CTkSlider):
    def __init__(self, container, espessura):
        super().__init__(container,
                         from_=1, to=30,
                         width=18,
                         variable=espessura,
                         number_of_steps=30,
                         orientation='vertical')

        self.place(x=48, y=190)

class EspessuraLabel(ctk.CTkLabel):
    def __init__(self, container, espessura):
        super().__init__(container, textvariable=espessura, text_color='white')
        x, y = 18, 390

        ctk.CTkLabel(container, text='Espessura: ').place(x=x, y=y)
        self.place(x=x+70, y=y)
