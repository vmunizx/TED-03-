"""Backup antes de modificar um arquivo existente."""
import shutil
from datetime import datetime
from pathlib import Path
import config


class BackupError(Exception):
    """Erro ao proteger os dados anteriores."""


def criar_backup(caminho, pasta_backup=None, avisar=True):
    origem = Path(caminho)
    if not origem.exists():
        if avisar:
            print(f'[INFO] {config.relativo(origem)} ainda não existe; backup desnecessário.')
        return None
    pasta = Path(pasta_backup) if pasta_backup is not None else config.PASTA_BACKUP
    try:
        pasta.mkdir(parents=True, exist_ok=True)
        carimbo = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        destino = pasta / f'{origem.stem}_{carimbo}{origem.suffix}'
        indice = 1
        while destino.exists():
            destino = pasta / f'{origem.stem}_{carimbo}_{indice}{origem.suffix}'
            indice += 1
        # shutil.copy2 preserva também os metadados; não abre arquivos diretamente.
        shutil.copy2(origem, destino)
    except OSError as erro:
        raise BackupError(f'Não foi possível criar backup de {config.relativo(origem)}: {erro}') from erro
    if avisar:
        print(f'[BACKUP] Cópia criada: {config.relativo(destino)}')
    return destino


# Mantém compatibilidade com o nome usado na versão inicial.
def realizar_backup(caminho_arquivo):
    return criar_backup(caminho_arquivo)
