import customtkinter as ctk
from canvas import AreaDeDesenho
from toolset import DrawTools
from pathlib import Path


class AppDesenho(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.title('Sem título - Desenhador 2D')

        self.largura = round(self.winfo_screenwidth() * 0.75)
        self.altura = round(self.winfo_screenheight() * 0.75)

        self.geometry(f'{self.largura}x{self.altura}')
        self.minsize(800, 600)

        self.resizable(False, False)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')

        self.iconbitmap(Path(__file__).parents[1] / "paint-pallete.ico")

        # dados
        self.espessura = ctk.IntVar(value=1)
        self.espessuraLabel = ctk.StringVar(value='')
        self.figura = ctk.StringVar(value='')

        # Componentes
        self.canvas = AreaDeDesenho(self, self.espessura, self.figura)
        self.drawtools = DrawTools(self, self.figura, self.canvas, self.espessura)

        self.bind("<Control-z>", self.canvas.desfaz)
        self.bind("<Control-l>", self.canvas.limpaTudo)

        self.mainloop()


if __name__ == '__main__':
    app = AppDesenho()
