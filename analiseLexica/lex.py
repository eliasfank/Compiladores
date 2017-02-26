import re

ENTRADA_FILE = 'entrada.txt'
CODIGO_FILE = 'codigo.txt'


FITA = {}
FITA['nomes'] = []
FITA['numeros'] = []


class Lex:
    VAR = '<var>'
    NUM = '<num>'
    SEP = ' ', '\n', '\t', '\r'
    FINAL = 'final'

    estados = []
    tokens = []
    automato = []
    simbolos = {}

    def __init__(self):
        self._le_arquivo()
        self._gera_automato()
        self._determiniza()

    def _gera_automato(self):
        FIRST = 0

        num_estado = 1
        self.automato.append({})

        for token in self.get_tokens():
            primeiro = True
            for c in token:
                if primeiro:
                    primeiro = False
                    if not self.automato[FIRST].get(c):
                        self.automato[FIRST].update({c: [num_estado]})
                    else:
                        self.automato[FIRST][c].append(num_estado)
                else:
                    num_estado += 1
                    self.automato.append({c: [num_estado]})

            self.automato.append({self.FINAL: token})
            num_estado += 1

        for key, val in self.simbolos.items():

            self.automato.append({self.FINAL: key})
            for i in val:

                if not self.automato[FIRST].get(i):
                    self.automato[FIRST].update({i: [num_estado]})
                else:
                    self.automato[FIRST][i].append(num_estado)

                self.automato[num_estado].update({i: [num_estado]})

            num_estado += 1

    def _determiniza(self):
        estados_a_adicionar = {}

        def modifica_automato(automato):
            prox_estado = len(automato)
            automato_aux = list(automato)
            x = 0 # se x for diferente de 0, refazer a funcao

            for i, transicao in enumerate(automato):

                for simbolo, estados in transicao.items():
                    if len(estados) > 1 and isinstance(estados, list):
                        print(simbolo, estados)

                        u = {}
                        for e in estados:
                            z = automato[e].copy()

                            for key, values in z.items():
                                if u.get(key):
                                    u[key].extend(values)
                                else:
                                    u.update({key: values})

                        estados_a_adicionar.update({simbolo: [prox_estado]})

                        automato_aux.append(u)

                        automato_aux[i].update(estados_a_adicionar)

                        return x, automato_aux
            x += 1
            return x, automato_aux

        x = 0
        while x == 0:
            x, self.automato = modifica_automato(self.automato)

    def _le_arquivo(self):
        for linha in self._abre_arquivo(ENTRADA_FILE):
            linha_partes = linha.split('::=')

            # pega o estado da gramatica antes do sinal ::=
            estado = linha_partes[0].strip()
            self.estados.append(estado)

            # pega os tokens de cada linha da gramatica
            linha_tokens = self._pega_tokens(linha_partes[1])

            if estado in [self.VAR, self.NUM]:
                var = linha_tokens[0].split(',')
                self.simbolos.update({estado: var})
            else:
                self.tokens.extend(linha_tokens)

    def _le_codigo(self):
        arquivo = self._abre_arquivo(CODIGO_FILE)

        for i, linha in enumerate(arquivo, start=1):
            estado = 0
            for c in linha:
                simbolos = self.automato[estado]

                if c in self.SEP:
                    FITA['nomes'].append(simbolos[self.FINAL])
                    FITA['numeros'].append(estado)
                    estado = 0
                elif simbolos.get(c):
                    estado = simbolos[c][0]
                    print(c, estado)
                else:
                    # erro de token invalido
                    msg = "erro na linha: {} , {}".format(i, linha)
                    print(msg)

    def _pega_tokens(self, linha):
        linha_comp = re.sub(r'<.*?>', ' ', linha)  # substitui os estados
        linha_comp = linha_comp.strip()
        linha_comp = linha_comp.replace('|', '')
        return linha_comp.split(' ')

    def _abre_arquivo(self, nome_arq):
        return open(nome_arq, 'r').readlines()

    def lex_print(self):
        for i, l in enumerate(self.automato):
            print(i, l)
    def print_fita(self):
        for k,v in FITA.items():
            print()
            print(k,v)
            print()

    def get_estados(self):
        return list(self.estados)

    def get_tokens(self):
        return list(self.tokens)


if __name__ == '__main__':
    lex = Lex()
    lex.lex_print()
    lex._le_codigo()
