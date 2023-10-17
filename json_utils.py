import json
from primitivos.graficos import *
from linked_list import LinkedList


def converte(cor_rgb: dict) -> str:
    string_rgb = "#"

    for cor in cor_rgb.values():
        string_rgb += f"{cor:02x}"

    return string_rgb


class JsonReader:
    @classmethod
    def read(cls, path):
        json_object = json.load(path)

        meu_desenho = json_object['desenho']
        p = None
        array_primitivos = LinkedList()
        for lista_primitivos in meu_desenho.keys():
            for primitivo in meu_desenho[lista_primitivos]:
                match primitivo['id'].split("_")[0]:
                    case 'ponto':
                        print('p')
                        p = PontoGr(x=primitivo['x'], y=primitivo['y'], cor=converte(primitivo['cor']),
                                    width=primitivo['esp'])
                    case 'reta':
                        print('r')
                        p = RetaGr(p1=Ponto(primitivo['p1']['x'], primitivo['p1']['y']),
                                   p2=Ponto(primitivo['p2']['x'], primitivo['p2']['y']),
                                   cor=converte(primitivo['cor']),width=primitivo['esp'])

                    case 'triang' | 'triangulo':
                        print('trg')
                        p = TrianguloGr([Ponto(primitivo['p1']['x'], primitivo['p1']['y']),
                                         Ponto(primitivo['p2']['x'], primitivo['p2']['y']),
                                         Ponto(primitivo['p3']['x'], primitivo['p3']['y'])],
                                        cor=converte(primitivo['cor']), width=primitivo['esp'])
                    case 'retang' | 'retangulo':
                        print("rtg")
                        p = RetanguloGr(p1=Ponto(primitivo['p1']['x'], primitivo['p1']['y']),
                                        p2=Ponto(primitivo['p2']['x'], primitivo['p2']['y']),
                                        cor=converte(primitivo['cor']), width=primitivo['esp'])
                    case 'circ' | 'circulo':
                        print('circ')
                        p = CirculoGr(Ponto(primitivo['centro']['x'], primitivo['centro']['y']),
                                      raio=primitivo['raio'], cor=converte(primitivo['cor']))
                    case 'mand' | 'mandala':
                        print('mand')

                if p is not None:
                    array_primitivos.append(p)

        return array_primitivos
