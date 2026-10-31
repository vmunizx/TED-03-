"""Backup automático: cria uma cópia com data e hora antes de qualquer alteração."""
import os
import shutil
from datetime import datetime

from config import PASTA_BACKUP, relativo


def realizar_backup(caminho_arquivo):
    """Copia o arquivo para a pasta de backups antes de ele ser alterado.

    Retorna o caminho do backup criado, ou None se o arquivo original ainda
    não existe (não há nada para preservar).
    Em caso de falha a exceção é relançada, para que quem chamou NÃO grave
    nada por cima dos dados originais.
    """
    if not os.path.exists(caminho_arquivo):
        return None

    try:
        os.makedirs(PASTA_BACKUP, exist_ok=True)

        nome, extensao = os.path.splitext(os.path.basename(caminho_arquivo))
        carimbo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        caminho_backup = os.path.join(PASTA_BACKUP, f"{nome}_{carimbo}{extensao}")

        with open(caminho_arquivo, "rb") as origem:
            with open(caminho_backup, "wb") as destino:
                shutil.copyfileobj(origem, destino)

        if os.path.getsize(caminho_arquivo) != os.path.getsize(caminho_backup):
            raise OSError("o backup foi criado, mas o tamanho difere do original")

        print(f"[BACKUP] Backup criado: {relativo(caminho_backup)}")
        return caminho_backup

    except PermissionError:
        print(f"[ERRO BACKUP] Sem permissão para criar backup de {relativo(caminho_arquivo)}")
        raise
    except OSError as erro:
        print(f"[ERRO BACKUP] Falha ao criar backup: {erro}")
        raise
