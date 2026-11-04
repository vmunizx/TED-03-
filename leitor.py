"""Leitura validada de arquivos CSV e JSON."""
import csv
import json
from config import ENCODING_LEITURA


def ler_csv(caminho):
    """Lê CSV com cabeçalho e devolve lista de dicionários."""
    with open(caminho, 'r', encoding=ENCODING_LEITURA, newline='') as arquivo:
        leitor = csv.DictReader(arquivo, strict=True)
        if not leitor.fieldnames or any(not c for c in leitor.fieldnames):
            raise ValueError('CSV vazio ou sem cabeçalho válido.')
        campos = list(leitor.fieldnames)
        registros = []
        for linha in leitor:
            if None in linha or any(valor is None for valor in linha.values()):
                raise ValueError('CSV com quantidade de colunas inconsistente.')
            registros.append(dict(linha))
    return registros


def ler_json(caminho):
    """Lê lista de objetos JSON."""
    with open(caminho, 'r', encoding=ENCODING_LEITURA) as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, list) or not all(isinstance(r, dict) for r in dados):
        raise ValueError('O JSON deve conter uma lista de objetos (registros).')
    return dados
