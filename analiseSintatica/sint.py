import json
import xmltodict

FITA = ['var', 'RECEBE', 'var', 'SE', 'num', 'IGUAL', 'var', 'ENTAO', 'var', 'RECEBE', 
        'num', 'SENAO', 'var', 'RECEBE', 'var', 'MAIS', 'num', 'var', 'RECEBE', 'num', 'MAIS', 'var', 'EOF']

ACTIONS = {
    'Shift': '1',
    'Reduce Rule': '2',
    'Goto': '3',
    'Accept': '4'
}

xml = open('gramatica.xml', 'r').read()
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

def tratarErro(in1, in2):
	if in1 == '25' and in2 == '14':
		print("Variável não pode receber variável!")


def analisaFita(fita):
    stack = [0]

    while fita:
        item = fita[0]

        state = stack[-1]

        index = mapa[item]
        action, value = get_action_value(state, index)


        if not action:
            print("Erro sintático!!")
            tratarErro(state, index)
            break

        if action == ACTIONS['Shift']:
            stack.append(value)
            print("shift ", value)
            fita.pop(0)
        elif action == ACTIONS['Reduce Rule']:

            # acessar o m_Production e pegar o indice que vem do value
            non_terminal, symbol_count = get_m_production(value)

            stack = stack[:len(stack) - int(symbol_count)]
            last_item_stack = stack[-1]

            action, value= get_action_value(last_item_stack, non_terminal)
            stack.append(value)

            print("reduce", value)

        elif action == ACTIONS['Accept']:
            print('Passou!')
            break
        else:
            break

mapa = mapeamento(m_Symbol)
#print(json.dumps(mapa, indent=4))
analisaFita(FITA)
