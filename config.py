"""Configuração de caminhos e codificação do projeto."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PASTA_DADOS = BASE_DIR / "dados"
PASTA_BACKUP = BASE_DIR / "backups"
ENCODING_LEITURA = "utf-8-sig"
ENCODING_ESCRITA = "utf-8"


def relativo(caminho):
    try:
        return str(Path(caminho).resolve().relative_to(BASE_DIR))
    except ValueError:
        return str(caminho)
