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

        self.resizable(False, False)
        self.pack_propagate(False)

        self.iconbitmap(Path(__file__).parent / "paint-pallete.ico")

        # dados
        self.espessura = ctk.IntVar(value=1)
        self.espessuraLabel = ctk.StringVar()
        self.figura = ctk.StringVar(value='')

        # Componentes
        self.canvas = AreaDeDesenho(self, self.espessura, self.figura)
        self.drawtools = DrawTools(self, self.figura, self.canvas, self.espessura)

        self.bind("<Control-z>", self.canvas.desfaz)
        self.bind("<Control-l>", self.canvas.limpaTudo)

        self.mainloop()


if __name__ == '__main__':
    app = AppDesenho()

