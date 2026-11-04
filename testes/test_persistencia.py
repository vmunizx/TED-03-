"""13 testes automatizados da TED 03, usando apenas a biblioteca padrão."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backup import BackupError
from conversor import csv_para_json, json_para_csv
from escritor import escrever_csv, escrever_json
from leitor import ler_csv, ler_json
from erros import executar, mensagem_erro


class TestPersistencia(unittest.TestCase):
    def setUp(self):
        pasta_temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(pasta_temporaria.cleanup)
        self.pasta = Path(pasta_temporaria.name)
        self.csv = self.pasta / 'clientes.csv'
        self.json = self.pasta / 'clientes.json'
        self.backups = self.pasta / 'backups'
        self.dados = [
            {'id': '1', 'nome': 'João', 'cidade': 'Balsas', 'valor': '150.50'},
            {'id': '2', 'nome': 'Conceição', 'cidade': 'São Luís', 'valor': '99.90'},
        ]

    def preparar_csv(self):
        with open(self.csv, 'w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=list(self.dados[0]))
            escritor.writeheader()
            escritor.writerows(self.dados)

    def preparar_json(self):
        with open(self.json, 'w', encoding='utf-8') as arquivo:
            json.dump(self.dados, arquivo, ensure_ascii=False)

    def test_csv_para_json_preserva_registros(self):
        self.preparar_csv()
        self.assertEqual(csv_para_json(self.csv, self.json, self.backups, False), 2)
        dados = ler_json(self.json)
        self.assertEqual(dados[0]['id'], 1)
        self.assertEqual(dados[0]['valor'], 150.5)
        self.assertEqual(dados[1]['nome'], 'Conceição')

    def test_json_para_csv(self):
        self.preparar_json()
        self.assertEqual(json_para_csv(self.json, self.csv, self.backups, False), 2)
        self.assertEqual(ler_csv(self.csv)[0]['valor'], '150.50')

    def test_ida_e_volta_sem_perda(self):
        self.preparar_csv()
        csv_para_json(self.csv, self.json, self.backups, False)
        destino = self.pasta / 'volta.csv'
        json_para_csv(self.json, destino, self.backups, False)
        self.assertEqual(ler_csv(self.csv), ler_csv(destino))

    def test_acentos_preservados_no_arquivo_json(self):
        escrever_json(self.dados, self.json, self.backups, False)
        self.assertIn('Conceição', self.json.read_text(encoding='utf-8'))

    def test_backup_criado_antes_de_sobrescrever(self):
        self.preparar_json()
        original = self.json.read_bytes()
        escrever_json([{'id': 9}], self.json, self.backups, False)
        copias = list(self.backups.glob('clientes_*.json'))
        self.assertEqual(len(copias), 1)
        self.assertEqual(copias[0].read_bytes(), original)

    def test_arquivo_novo_nao_gera_backup(self):
        escrever_json(self.dados, self.json, self.backups, False)
        self.assertFalse(self.backups.exists())

    def test_falha_no_backup_impede_a_escrita(self):
        self.preparar_json()
        original = self.json.read_bytes()
        with patch('escritor.criar_backup', side_effect=BackupError('falha simulada')):
            with self.assertRaises(BackupError):
                escrever_json([{'id': 9}], self.json, self.backups, False)
        self.assertEqual(self.json.read_bytes(), original)

    def test_arquivo_nao_encontrado(self):
        ok, _ = executar(ler_csv, self.pasta / 'nao_existe.csv')
        self.assertFalse(ok)
        self.assertIn('não encontrado', mensagem_erro(FileNotFoundError()))

    def test_permissao_negada(self):
        with patch('builtins.open', side_effect=PermissionError('negado')):
            ok, _ = executar(ler_csv, self.csv)
        self.assertFalse(ok)
        self.assertIn('permissão', mensagem_erro(PermissionError()))

    def test_codificacao_invalida(self):
        self.csv.write_bytes('nome\nConceição\n'.encode('latin-1'))
        ok, _ = executar(ler_csv, self.csv)
        self.assertFalse(ok)

    def test_json_malformado(self):
        self.json.write_text('{"nome": "João",}', encoding='utf-8')
        with self.assertRaises(json.JSONDecodeError):
            ler_json(self.json)

    def test_json_que_nao_e_lista_de_objetos(self):
        self.json.write_text('{"nome": "João"}', encoding='utf-8')
        with self.assertRaises(ValueError):
            ler_json(self.json)

    def test_csv_vazio(self):
        self.csv.write_text('', encoding='utf-8')
        with self.assertRaises(ValueError):
            ler_csv(self.csv)


if __name__ == '__main__':
    unittest.main()
