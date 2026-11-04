"""Gravação protegida de CSV e JSON usando with open."""
import csv
import json
from pathlib import Path
from backup import criar_backup
from config import ENCODING_ESCRITA, relativo


def _preparar(caminho, pasta_backup=None, avisar=True):
    # Se o arquivo já existe e o backup falha, a escrita não começa.
    copia = criar_backup(caminho, pasta_backup, avisar)
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    return copia


def escrever_json(dados, caminho, pasta_backup=None, avisar=True):
    # Serializa antes do backup e antes de tocar no arquivo de destino.
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    _preparar(caminho, pasta_backup, avisar)
    with open(caminho, 'w', encoding=ENCODING_ESCRITA) as arquivo:
        arquivo.write(texto)
    if avisar:
        print(f'[OK] JSON gravado: {relativo(caminho)}')
    return True


def escrever_csv(dados, caminho, pasta_backup=None, avisar=True):
    if not dados:
        raise ValueError('Não é possível escrever CSV sem registros e cabeçalho.')
    if not all(isinstance(item, dict) for item in dados):
        raise ValueError('Cada registro CSV deve ser um dicionário.')
    campos = list(dict.fromkeys(campo for registro in dados for campo in registro))
    if not campos:
        raise ValueError('Os registros CSV precisam ter campos.')
    _preparar(caminho, pasta_backup, avisar)
    with open(caminho, 'w', encoding=ENCODING_ESCRITA, newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)
    if avisar:
        print(f'[OK] CSV gravado: {relativo(caminho)}')
    return True
