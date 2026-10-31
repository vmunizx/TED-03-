"""Conversão entre CSV e JSON."""
from escritor import escrever_csv, escrever_json
from leitor import ler_csv, ler_json


def _converter_tipos(registro):
    """O CSV guarda tudo como texto. Aqui 'id' vira int e 'valor' vira float
    quando possível; se algum campo não puder ser convertido, ele é mantido
    como texto (nenhuma informação é perdida)."""
    novo = dict(registro)
    for campo, tipo in (("id", int), ("valor", float)):
        try:
            novo[campo] = tipo(novo[campo])
        except (KeyError, ValueError, TypeError):
            pass
    return novo


def csv_para_json(caminho_csv, caminho_json):
    print("\n--- Convertendo CSV -> JSON ---")
    dados = [_converter_tipos(reg) for reg in ler_csv(caminho_csv)]
    if escrever_json(dados, caminho_json):
        print(f"Conversão concluída: {len(dados)} registros convertidos.")


def json_para_csv(caminho_json, caminho_csv):
    print("\n--- Convertendo JSON -> CSV ---")
    dados = ler_json(caminho_json)
    if not all(isinstance(reg, dict) for reg in dados):
        print("[ERRO] Cada item do JSON deve ser um objeto (registro com campos).")
        raise ValueError("JSON com itens que não são registros")
    if escrever_csv(dados, caminho_csv):
        print(f"Conversão concluída: {len(dados)} registros convertidos.")
