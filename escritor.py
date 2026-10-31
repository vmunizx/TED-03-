"""Escrita de arquivos CSV e JSON, sempre precedida de backup."""
import csv
import json

from backup import realizar_backup
from config import relativo


def escrever_json(dados, caminho):
    """Grava a lista de registros em JSON (UTF-8, acentos preservados).

    Retorna True se gravou.
    """
    try:
        # Backup ANTES de alterar. Se falhar, a exceção interrompe tudo aqui
        # e o arquivo original não é tocado.
        realizar_backup(caminho)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"[ESCRITA] Dados gravados em {relativo(caminho)}")
        return True
    except PermissionError:
        print(f"[ERRO] Sem permissão para escrever: {relativo(caminho)}")
        raise
    except (OSError, TypeError) as erro:
        print(f"[ERRO] Falha ao escrever JSON: {erro}")
        raise


def _campos_do_csv(dados):
    """Une as chaves de todos os registros, mantendo a ordem em que aparecem."""
    campos = []
    for registro in dados:
        for chave in registro:
            if chave not in campos:
                campos.append(chave)
    return campos


def escrever_csv(dados, caminho):
    """Grava a lista de registros em CSV (UTF-8). Retorna True se gravou."""
    if not dados:
        print("[AVISO] Nenhum dado para escrever. O arquivo não foi alterado.")
        return False

    try:
        realizar_backup(caminho)

        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=_campos_do_csv(dados))
            escritor.writeheader()
            escritor.writerows(dados)
        print(f"[ESCRITA] Dados gravados em {relativo(caminho)}")
        return True
    except PermissionError:
        print(f"[ERRO] Sem permissão para escrever: {relativo(caminho)}")
        raise
    except (OSError, csv.Error) as erro:
        print(f"[ERRO] Falha ao escrever CSV: {erro}")
        raise
