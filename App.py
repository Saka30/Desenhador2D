import customtkinter as ctk
from canvas import AreaDeDesenho
from toolset import DrawTools
import os


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

        # configura o diretorio do icone indepedente da IDE
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.script_dir, "paint-pallete.ico")
        self.iconbitmap(self.icon_path)

        # dados
        self.espessura = ctk.IntVar(value=1)
        self.espessuraLabel = ctk.StringVar()
        self.figura = ctk.StringVar(value='')

        # Componentes
        self.canvas = AreaDeDesenho(self, self.espessura, self.figura)
        self.drawtools = DrawTools(self, self.figura, self.canvas, self.espessura)

        self.bind("<Control-z>", self.canvas.desfaz)
        self.bind("<Control-l>", self.canvas.limpaTudo)


if __name__ == '__main__':
    app = AppDesenho()
    app.mainloop()
