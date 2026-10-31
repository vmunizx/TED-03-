"""TED-03 - Gerenciador de Persistência de Dados (CSV e JSON)."""
import csv
import json
import os

from config import PASTA_DADOS
from conversor import csv_para_json, json_para_csv
from escritor import escrever_csv
from leitor import ler_csv, ler_json

CSV_CLIENTES = os.path.join(PASTA_DADOS, "clientes.csv")
JSON_CLIENTES = os.path.join(PASTA_DADOS, "clientes.json")
CSV_CONVERTIDO = os.path.join(PASTA_DADOS, "clientes_convertido.csv")
JSON_CONVERTIDO = os.path.join(PASTA_DADOS, "clientes_convertido.json")

# Arquivos usados só para demonstrar o tratamento de erros
CSV_INEXISTENTE = os.path.join(PASTA_DADOS, "nao_existe.csv")
JSON_MALFORMADO = os.path.join(PASTA_DADOS, "erros", "malformado.json")
CSV_LATIN1 = os.path.join(PASTA_DADOS, "erros", "latin1.csv")

ERROS_TRATADOS = (
    FileNotFoundError,
    PermissionError,
    UnicodeDecodeError,
    json.JSONDecodeError,
    csv.Error,
    ValueError,
    OSError,
)


def adicionar_cliente():
    """Lê o CSV, acrescenta um cliente e grava (o backup é feito pelo escritor)."""
    dados = ler_csv(CSV_CLIENTES)

    nome = input("Nome: ").strip()
    cidade = input("Cidade: ").strip()
    valor_texto = input("Valor: ").strip().replace(",", ".")

    if not nome or not cidade:
        print("[AVISO] Nome e cidade são obrigatórios. Nada foi alterado.")
        return
    try:
        valor = float(valor_texto)
    except ValueError:
        print("[AVISO] Valor inválido (use números, ex.: 99.90). Nada foi alterado.")
        return

    ids_existentes = [int(reg["id"]) for reg in dados if reg.get("id", "").isdigit()]
    novo_id = max(ids_existentes, default=0) + 1
    dados.append({"id": str(novo_id), "nome": nome, "cidade": cidade, "valor": f"{valor:.2f}"})
    escrever_csv(dados, CSV_CLIENTES)


def menu():
    while True:
        print("\n===== TED-03 GERENCIADOR DE PERSISTENCIA =====")
        print("1 - Converter CSV para JSON")
        print("2 - Converter JSON para CSV")
        print("3 - Adicionar novo cliente (testa backup)")
        print("4 - Simular erro: arquivo inexistente (FileNotFoundError)")
        print("5 - Simular erro: JSON malformado")
        print("6 - Simular erro: codificação inválida (UnicodeDecodeError)")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            print("Encerrando.")
            break

        try:
            if opcao == "1":
                csv_para_json(CSV_CLIENTES, JSON_CONVERTIDO)
            elif opcao == "2":
                json_para_csv(JSON_CLIENTES, CSV_CONVERTIDO)
            elif opcao == "3":
                adicionar_cliente()
            elif opcao == "4":
                ler_csv(CSV_INEXISTENTE)
            elif opcao == "5":
                ler_json(JSON_MALFORMADO)
            elif opcao == "6":
                ler_csv(CSV_LATIN1)
            else:
                print("Opção inválida. Escolha um número do menu.")
        except ERROS_TRATADOS:
            # A mensagem detalhada já foi mostrada pelo módulo que detectou o erro.
            print("Operação cancelada. Voltando ao menu.")
        except Exception as erro:
            print(f"[ERRO INESPERADO] {erro}. Voltando ao menu.")


if __name__ == "__main__":
    menu()
