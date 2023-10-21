import json
from primitivos.graficos import *
from linked_list import LinkedList


def converte(cor_rgb: dict) -> str:
    string_rgb = "#"

    for cor in cor_rgb.values():
        string_rgb += f"{cor:02x}"

    return string_rgb


def ajustar_coordenadas(coordenadas: dict) -> Ponto:

    x = round(coordenadas['x'] * 800)
    y = round(coordenadas['y'] * 600)

    return Ponto(x, y)


class JsonHandler:
    @classmethod
    def read(cls, file_json) -> LinkedList:
        json_object = json.load(file_json)
        meu_desenho = json_object['desenho']
        p = None
        array_primitivos = LinkedList()

        for lista_primitivos in meu_desenho.keys():
            for primitivo in meu_desenho[lista_primitivos]:
                match lista_primitivos:
                    case 'ponto':
                        coordenada = ajustar_coordenadas(primitivo)
                        p = PontoGr(x=coordenada.x, y=coordenada.y, cor=converte(primitivo['cor']),
                                    width=primitivo['esp'])
                    case 'reta':
                        coordenadas = (ajustar_coordenadas(primitivo['p1']), ajustar_coordenadas(primitivo['p2']))
                        p = RetaGr(p1=coordenadas[0],p2=coordenadas[1],
                                   cor=converte(primitivo['cor']), width=primitivo['esp'])
                    case 'triangulo':
                        coordenadas = [ajustar_coordenadas(primitivo[pt]) for pt in ['p1','p2','p3']]
                        p = TrianguloGr(coordenadas,cor=converte(primitivo['cor']), width=primitivo['esp'])
                    case 'retangulo':
                        coordenadas = (ajustar_coordenadas(primitivo['p1']), ajustar_coordenadas(primitivo['p2']))
                        p = RetanguloGr(p1=coordenadas[0], p2=coordenadas[1],
                                        cor=converte(primitivo['cor']), width=primitivo['esp'])
                    case 'circulo':
                        centro = ajustar_coordenadas(primitivo['centro'])
                        raio = ajustar_coordenadas({'x':primitivo['raio'], 'y':0})
                        p = CirculoGr(centro=centro, raio=raio.x, cor=converte(primitivo['cor']),
                                      width=primitivo['esp'])

                    case 'mandala':
                        centro = ajustar_coordenadas(primitivo['p1'])
                        p2 = ajustar_coordenadas(primitivo['p2'])

                        p = Mandala(p1=centro, p2=p2, corCirc=converte(primitivo['cor1']),
                                    corRetas=converte(primitivo['cor2']), width=primitivo['esp'])

                if p is not None:
                    array_primitivos.append(p)

        return array_primitivos

    @classmethod
    def write(cls, path:str, ed:LinkedList):
        desenho = {'desenho':{}}
        meu_desenho = desenho['desenho']

        for i in range(len(ed)):
            primitivo = ed[i]
            if primitivo.tipo not in meu_desenho.keys():
                meu_desenho[primitivo.tipo] = []

            meu_desenho[primitivo.tipo].append(primitivo.info())

        json_object = json.dumps(desenho, indent=4)

        with open(path, 'w') as json_file:
            json_file.write(json_object)

