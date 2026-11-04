"""Conversao segura entre arquivos CSV e JSON."""

from escritor import escrever_csv, escrever_json
from leitor import ler_csv, ler_json


def _converter_tipos(registro):
    """Converte id para inteiro e valor para decimal."""
    novo = dict(registro)

    try:
        novo["id"] = int(novo["id"])
    except (KeyError, ValueError, TypeError):
        pass

    try:
        novo["valor"] = float(
            str(novo["valor"]).replace(",", ".")
        )
    except (KeyError, ValueError, TypeError):
        pass

    return novo


def _formatar_registro(registro):
    """Prepara valores para escrita no CSV."""
    novo = dict(registro)

    if "valor" in novo:
        valor = novo["valor"]

        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            novo["valor"] = f"{valor:.2f}"

    return novo


def csv_para_json(caminho_csv, caminho_json):
    """Converte registros CSV em JSON."""
    print("\n--- Convertendo CSV -> JSON ---")

    registros = ler_csv(caminho_csv)
    dados = [_converter_tipos(r) for r in registros]

    if escrever_json(dados, caminho_json):
        print(
            f"[OK] Conversao concluida: "
            f"{len(dados)} registros."
        )
        return len(dados)

    return 0


def json_para_csv(caminho_json, caminho_csv):
    """Converte registros JSON em CSV."""
    print("\n--- Convertendo JSON -> CSV ---")

    dados = ler_json(caminho_json)

    if not all(isinstance(r, dict) for r in dados):
        raise ValueError(
            "O JSON deve conter apenas objetos."
        )

    registros = [_formatar_registro(r) for r in dados]

    if escrever_csv(registros, caminho_csv):
        print(
            f"[OK] Conversao concluida: "
            f"{len(registros)} registros."
        )
        return len(registros)

    return 0
