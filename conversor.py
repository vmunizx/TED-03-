"""Conversão entre CSV e JSON para cadastros de clientes."""
from leitor import ler_csv, ler_json
from escritor import escrever_csv, escrever_json


def _converter_tipos(registro):
    novo = dict(registro)
    try:
        novo['id'] = int(novo['id'])
    except (KeyError, ValueError, TypeError):
        pass
    try:
        novo['valor'] = float(str(novo['valor']).replace(',', '.'))
    except (KeyError, ValueError, TypeError):
        pass
    return novo


def _para_csv(registro):
    novo = dict(registro)
    valor = novo.get('valor')
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        novo['valor'] = f'{valor:.2f}'
    return novo


def csv_para_json(origem, destino, pasta_backup=None, avisar=True):
    dados = [_converter_tipos(registro) for registro in ler_csv(origem)]
    escrever_json(dados, destino, pasta_backup, avisar)
    return len(dados)


def json_para_csv(origem, destino, pasta_backup=None, avisar=True):
    dados = [_para_csv(registro) for registro in ler_json(origem)]
    escrever_csv(dados, destino, pasta_backup, avisar)
    return len(dados)
