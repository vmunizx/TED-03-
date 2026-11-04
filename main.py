"""Menu de demonstração da TED 03 - persistência CSV/JSON."""
from pathlib import Path
from config import PASTA_DADOS, PASTA_BACKUP
from conversor import csv_para_json, json_para_csv
from escritor import escrever_csv
from leitor import ler_csv, ler_json
from erros import executar

CSV_CLIENTES = PASTA_DADOS / 'clientes.csv'
JSON_CLIENTES = PASTA_DADOS / 'clientes.json'
CSV_CONVERTIDO = PASTA_DADOS / 'clientes_convertido.csv'
JSON_CONVERTIDO = PASTA_DADOS / 'clientes_convertido.json'


def adicionar_cliente():
    dados = ler_csv(CSV_CLIENTES)
    nome = input('Nome: ').strip()
    cidade = input('Cidade: ').strip()
    valor_texto = input('Valor: ').strip().replace(',', '.')
    if not nome or not cidade:
        raise ValueError('Nome e cidade são obrigatórios.')
    try:
        valor = float(valor_texto)
    except ValueError as erro:
        raise ValueError('Valor deve ser numérico (ex.: 99.90).') from erro
    ids = [int(r['id']) for r in dados if str(r.get('id', '')).isdigit()]
    novo = {'id': str(max(ids, default=0) + 1), 'nome': nome,
            'cidade': cidade, 'valor': f'{valor:.2f}'}
    # Preenche quaisquer campos extras que já existam no arquivo.
    if dados:
        novo = {chave: novo.get(chave, '') for chave in dados[0]}
    dados.append(novo)
    escrever_csv(dados, CSV_CLIENTES)
    print('[OK] Cliente adicionado.')


def exibir_csv():
    for registro in ler_csv(CSV_CLIENTES):
        print(registro)


def listar_backups():
    arquivos = sorted(PASTA_BACKUP.glob('*')) if PASTA_BACKUP.exists() else []
    if not arquivos:
        print('[INFO] Ainda não há backups.')
    for arquivo in arquivos:
        if arquivo.is_file():
            print(arquivo.name)


def executar_opcao(opcao):
    if opcao == '1':
        return executar(csv_para_json, CSV_CLIENTES, JSON_CONVERTIDO, caminho=CSV_CLIENTES)
    if opcao == '2':
        return executar(json_para_csv, JSON_CLIENTES, CSV_CONVERTIDO, caminho=JSON_CLIENTES)
    if opcao == '3':
        return executar(adicionar_cliente, caminho=CSV_CLIENTES)
    if opcao == '4':
        return executar(ler_csv, PASTA_DADOS / 'arquivo_que_nao_existe.csv', caminho=PASTA_DADOS / 'arquivo_que_nao_existe.csv')
    if opcao == '5':
        caminho = PASTA_DADOS / 'erros' / 'malformado.json'
        return executar(ler_json, caminho, caminho=caminho)
    if opcao == '6':
        caminho = PASTA_DADOS / 'erros' / 'latin1.csv'
        return executar(ler_csv, caminho, caminho=caminho)
    if opcao == '7':
        return executar(listar_backups)
    if opcao == '8':
        return executar(exibir_csv)
    print('[AVISO] Escolha uma opção válida.')
    return False, None


def menu():
    acoes = ['1 - Converter CSV para JSON', '2 - Converter JSON para CSV',
             '3 - Adicionar cliente (gera backup)', '4 - Simular arquivo inexistente',
             '5 - Simular JSON malformado', '6 - Simular codificação inválida',
             '7 - Listar backups', '8 - Exibir clientes.csv', '0 - Sair']
    while True:
        print('\n===== TED 03 =====')
        print('\n'.join(acoes))
        opcao = input('Escolha: ').strip()
        if opcao == '0':
            break
        executar_opcao(opcao)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        executar_opcao(sys.argv[1])
    else:
        menu()
