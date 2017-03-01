import json

import xmltodict
# from collections import queue

FITA = ['SE', 'num', 'IGUAL', 'var', 'ENTAO', 'var', 'RECEBE', 'num', 'SENAO', 'var', 'RECEBE', 'num']


# FITA = ['enquanto', 'identificador', '>', 'identificador', 'fazer',
#         'identificador', 'atribuir', 'numero', 'fim', 'EOF']


ACTIONS = {
    'Shift': '1',
    'Reduce Rule': '2',
    'Goto': '3',
    'Accept': '4'
}

xml = open('gramatica.xml', 'r').read()
# xml = open('teste.xml', 'r').read()
dict_xml = xmltodict.parse(xml)


def LALRStates():
    states = dict_xml['Tables']['LALRTable']['LALRState']
    return states


def get_m_production(index):
    production = dict_xml['Tables']['m_Production']['Production']
    production = production[int(index)]
    return production['@NonTerminalIndex'], production['@SymbolCount']


def get_action_value(state, symbol_index):
    actions = LALRStates()[int(state)]['LALRAction']
    if not isinstance(actions, list):
        if actions['@SymbolIndex'] == symbol_index:
            return actions['@Action'], actions['@Value']
    else:
        for action in actions:
            if action['@SymbolIndex'] == symbol_index:
                return action['@Action'], action['@Value']
    return None, None

m_Symbol = dict_xml['Tables']['m_Symbol']['Symbol']


def mapeamento(symbols):
    data = {}
    for symbol in symbols:
        data.update({
            symbol['@Name']: symbol['@Index']
        })
    return data


def analisaFita(fita):
    stack = [0]

    while fita:
        item = fita[0]

        state = stack[-1]
        # if state != 0:
        #     state = mapa[state]

        index = mapa[item]
        action, value = get_action_value(state, index)

        if action == ACTIONS['Shift']:
            # stack.append(item)
            stack.append(value)
            fita.pop(0)
        elif action == ACTIONS['Reduce Rule']:

            # acessar o m_Production e pegar o indice que vem do value
            non_terminal, symbol_count = get_m_production(value)

            # tirar da stack 2 * @SymbolCount
            stack = stack[:len(stack) - int(symbol_count)]
            stack.append(non_terminal)

            last_item_stack = stack[-1]

            action, value= get_action_value(last_item_stack, non_terminal)

            # stack.append(value)

            print(state)
        elif action == ACTIONS['Accept']:
            print('Passou!')
        else:
            break

mapa = mapeamento(m_Symbol)
print(json.dumps(mapa, indent=4))

analisaFita(FITA)
