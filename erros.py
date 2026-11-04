"""Mensagens amigáveis para os erros do gerenciador."""
import csv
import json
from backup import BackupError
from config import relativo


def mensagem_erro(erro, caminho=None):
    onde = f' ({relativo(caminho)})' if caminho is not None else ''
    if isinstance(erro, BackupError):
        return f'{erro}. A operação foi cancelada antes da gravação.'
    if isinstance(erro, FileNotFoundError):
        return f'Arquivo não encontrado{onde}. Confira a pasta e o nome.'
    if isinstance(erro, PermissionError):
        return f'Sem permissão para acessar ou modificar o arquivo{onde}.'
    if isinstance(erro, IsADirectoryError):
        return f'O caminho informado é uma pasta, e não um arquivo{onde}.'
    if isinstance(erro, UnicodeDecodeError):
        return f'Erro de codificação UTF-8{onde}. Verifique a codificação do arquivo.'
    if isinstance(erro, json.JSONDecodeError):
        return f'JSON malformado{onde}: linha {erro.lineno}, coluna {erro.colno}.'
    if isinstance(erro, csv.Error):
        return f'CSV inválido{onde}: {erro}'
    if isinstance(erro, ValueError):
        return f'Dados inválidos{onde}: {erro}'
    if isinstance(erro, OSError):
        return f'Erro de entrada/saída{onde}: {erro}'
    return f'Erro inesperado: {erro}'


def executar(operacao, *args, caminho=None, **kwargs):
    try:
        return True, operacao(*args, **kwargs)
    except (OSError, ValueError, csv.Error, BackupError, TypeError) as erro:
        print('[ERRO]', mensagem_erro(erro, caminho))
        return False, None
