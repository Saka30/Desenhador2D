import json
from primitivos.graficos import *
from linked_list import LinkedList


def converte(cor_rgb: dict) -> str:
    string_rgb = "#"

    for cor in cor_rgb.values():
        string_rgb += f"{cor:02x}"

    return string_rgb


class JsonHandler:

    def __init__(self, canvas):
        self.canvas = canvas

    def read(self, file_json) -> LinkedList:
        json_object = json.load(file_json)
        meu_desenho = json_object['desenho']
        p = None
        array_primitivos = LinkedList()

        for lista_primitivos in meu_desenho.keys():
            for primitivo in meu_desenho[lista_primitivos]:
                match lista_primitivos:
                    case 'ponto':
                        coordenada = self.ajustar_coordenadas(primitivo)
                        p = PontoGr(x=coordenada.x, y=coordenada.y, cor=converte(primitivo['cor']),
                                    width=round(primitivo['esp'] / 100 * 30))
                    case 'reta':
                        coordenadas = (self.ajustar_coordenadas(primitivo['p1']), self.ajustar_coordenadas(primitivo['p2']))
                        p = RetaGr(p1=coordenadas[0], p2=coordenadas[1],
                                   cor=converte(primitivo['cor']), width=round(primitivo['esp'] / 100 * 30))
                    case 'triangulo':
                        coordenadas = [self.ajustar_coordenadas(primitivo[pt]) for pt in ['p1', 'p2', 'p3']]
                        p = TrianguloGr(coordenadas, cor=converte(primitivo['cor']),
                                        width=round(primitivo['esp'] / 100 * 30))
                    case 'retangulo':
                        coordenadas = (self.ajustar_coordenadas(primitivo['p1']), self.ajustar_coordenadas(primitivo['p2']))
                        p = RetanguloGr(p1=coordenadas[0], p2=coordenadas[1],
                                        cor=converte(primitivo['cor']), width=round(primitivo['esp'] / 100 * 30))
                    case 'circulo':
                        centro = self.ajustar_coordenadas(primitivo['centro'])
                        raio = primitivo['raio'] * self.canvas.largura
                        p = CirculoGr(centro=centro, raio=raio, cor=converte(primitivo['cor']),
                                      width=round(primitivo['esp'] / 100 * 30))

                    case 'mandala':
                        centro = self.ajustar_coordenadas(primitivo['p1'])
                        p2 = self.ajustar_coordenadas(primitivo['p2'])

                        p = Mandala(p1=centro, p2=p2, corCirc=converte(primitivo['cor1']),
                                    corRetas=converte(primitivo['cor2']), width=round(primitivo['esp'] / 100 * 30))

                if p is not None:
                    array_primitivos.append(p)

        return array_primitivos

    def write(self, path: str, ed: LinkedList) -> None:
        desenho = {'desenho': {}}
        meu_desenho = desenho['desenho']

        for i in range(len(ed)):
            primitivo = ed[i]
            meu_desenho.setdefault(primitivo.tipo, []).append(primitivo.info(self.canvas))

        json_object = json.dumps(desenho, indent=4)

        with open(path, 'w') as json_file:
            json_file.write(json_object)

    def ajustar_coordenadas(self, coordenadas: dict) -> Ponto:

        x = round(coordenadas['x'] * self.canvas.largura)
        y = round(coordenadas['y'] * self.canvas.altura)

        return Ponto(x, y)
