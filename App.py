'''
data 05/09/2023
Integrantes do Grupo - Turma B:
   -Gabriel Carlos Silva -  RA00325868
   -Gustavo Bertolini Carvalho de Castro - RA00325934
   -Rafael Santos Sakatauskas  - RA00325920
'''

import customtkinter as ctk
from canvas import AreaDeDesenho
from toolset import DrawTools
import os


class AppDesenho(ctk.CTk):
    def __init__(self, largura, altura):
        super().__init__()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.title('Sem título - Desenhador 2D')
        self.geometry(f'{largura}x{altura}')
        self.resizable(False, False)
        self.pack_propagate(False)

        #configura o diretorio do icone indepedente da IDE
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.script_dir, "paint-pallete.ico")
        self.iconbitmap(self.icon_path)

        #dados
        self.espessura = ctk.IntVar(value=1)
        self.espessuraLabel = ctk.StringVar()
        self.figura = ctk.StringVar(value='')

        # Componentes
        self.canvas = AreaDeDesenho(self, self.espessura, self.figura)
        self.drawtools = DrawTools(self, self.figura, self.canvas, self.espessura)


        self.mainloop()


if __name__ == '__main__':
    AppDesenho(800, 600)

