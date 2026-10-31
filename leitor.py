"""Leitura de arquivos CSV e JSON."""
import csv
import json

from config import relativo

# "utf-8-sig" é UTF-8 que também aceita o BOM que o Excel costuma colocar
# no início de CSVs. Em arquivos UTF-8 normais funciona de forma idêntica.
CODIFICACAO_LEITURA = "utf-8-sig"


def ler_csv(caminho):
    """Lê um CSV e devolve uma lista de dicionários (um por linha)."""
    try:
        with open(caminho, "r", encoding=CODIFICACAO_LEITURA, newline="") as arquivo:
            dados = list(csv.DictReader(arquivo))
        print(f"[LEITURA] {len(dados)} registros lidos de {relativo(caminho)}")
        return dados
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {relativo(caminho)}")
        raise
    except PermissionError:
        print(f"[ERRO] Sem permissão para ler: {relativo(caminho)}")
        raise
    except UnicodeDecodeError:
        print(f"[ERRO] Erro de codificação (o arquivo não está em UTF-8): {relativo(caminho)}")
        raise
    except csv.Error as erro:
        print(f"[ERRO] CSV inválido em {relativo(caminho)}: {erro}")
        raise


def ler_json(caminho):
    """Lê um JSON que contenha uma lista de registros e devolve essa lista."""
    try:
        with open(caminho, "r", encoding=CODIFICACAO_LEITURA) as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {relativo(caminho)}")
        raise
    except PermissionError:
        print(f"[ERRO] Sem permissão para ler: {relativo(caminho)}")
        raise
    except UnicodeDecodeError:
        print(f"[ERRO] Erro de codificação (o arquivo não está em UTF-8): {relativo(caminho)}")
        raise
    except json.JSONDecodeError as erro:
        print(f"[ERRO] JSON malformado em {relativo(caminho)} (linha {erro.lineno}, coluna {erro.colno})")
        raise

    if not isinstance(dados, list):
        print(f"[ERRO] O JSON deve conter uma lista de registros: {relativo(caminho)}")
        raise ValueError("estrutura JSON inesperada: esperava uma lista de registros")

    print(f"[LEITURA] {len(dados)} registros lidos de {relativo(caminho)}")
    return dados
