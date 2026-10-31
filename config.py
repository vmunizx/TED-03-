"""Configurações de caminhos do projeto.

Os caminhos são calculados a partir da pasta deste arquivo, então o programa
funciona mesmo que seja executado de outro diretório.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")
PASTA_BACKUP = os.path.join(BASE_DIR, "backups")


def relativo(caminho):
    """Retorna o caminho relativo ao projeto (mensagens mais curtas e legíveis)."""
    return os.path.relpath(caminho, BASE_DIR)
