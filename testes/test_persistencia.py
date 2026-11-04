
"""Testes automatizados da TED 03 - CSV, JSON e backup."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Permite importar os modulos da pasta principal.
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import backup
from conversor import csv_para_json, json_para_csv
from escritor import escrever_csv, escrever_json
from leitor import ler_csv, ler_json


class TestPersistencia(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)
        self.csv = self.pasta / "clientes.csv"
        self.json = self.pasta / "clientes.json"
        self.backups = self.pasta / "backups"

        self.patch_backup = patch.object(
            backup, "PASTA_BACKUP", str(self.backups)
        )
        self.patch_backup.start()
        self.addCleanup(self.patch_backup.stop)

        self.dados = [
            {
                "id": "1",
                "nome": "João",
                "cidade": "Balsas",
                "valor": "150.50",
            },
            {
                "id": "2",
                "nome": "Conceição",
                "cidade": "São Luís",
                "valor": "99.90",
            },
        ]

    def preparar_csv(self):
        with open(self.csv, "w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(
                f, fieldnames=list(self.dados[0].keys())
            )
            escritor.writeheader()
            escritor.writerows(self.dados)

    def preparar_json(self):
        with open(self.json, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False)

    def test_01_csv_para_json(self):
        self.preparar_csv()
        csv_para_json(self.csv, self.json)
        dados = ler_json(self.json)
        self.assertEqual(len(dados), 2)
        self.assertEqual(dados[0]["id"], 1)
        self.assertEqual(dados[0]["valor"], 150.50)

    def test_02_json_para_csv(self):
        self.preparar_json()
        json_para_csv(self.json, self.csv)
        dados = ler_csv(self.csv)
        self.assertEqual(len(dados), 2)
        self.assertEqual(dados[0]["nome"], "João")

    def test_03_ida_e_volta(self):
        self.preparar_csv()
        csv_para_json(self.csv, self.json)
        destino = self.pasta / "resultado.csv"
        json_para_csv(self.json, destino)
        dados = ler_csv(destino)
        self.assertEqual(len(dados), len(self.dados))
        self.assertEqual(dados[0]["nome"], "João")

    def test_04_acentos_preservados(self):
        escrever_json(self.dados, self.json)
        with open(self.json, "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("Conceição", conteudo)
        self.assertIn("João", conteudo)

    def test_05_backup_antes_de_sobrescrever(self):
        self.preparar_json()
        original = self.json.read_bytes()
        escrever_json([{"id": 99}], self.json)
        arquivos = list(self.backups.glob("clientes_*.json"))
        self.assertEqual(len(arquivos), 1)
        self.assertEqual(arquivos[0].read_bytes(), original)

    def test_06_arquivo_novo_sem_backup(self):
        escrever_json(self.dados, self.json)
        self.assertTrue(self.json.exists())
        self.assertFalse(self.backups.exists())

    def test_07_falha_backup_impede_escrita(self):
        self.preparar_json()
        original = self.json.read_bytes()
        with patch(
            "escritor.realizar_backup",
            side_effect=OSError("Falha simulada")
        ):
            with self.assertRaises(OSError):
                escrever_json([{"id": 99}], self.json)
        self.assertEqual(self.json.read_bytes(), original)

    def test_08_arquivo_nao_encontrado(self):
        with self.assertRaises(FileNotFoundError):
            ler_csv(self.pasta / "inexistente.csv")

    def test_09_permissao_negada(self):
        with patch(
            "builtins.open",
            side_effect=PermissionError("Acesso negado")
        ):
            with self.assertRaises(PermissionError):
                ler_csv(self.csv)

    def test_10_codificacao_invalida(self):
        self.csv.write_bytes(
            "nome\nConceição\n".encode("latin-1")
        )
        with self.assertRaises(UnicodeDecodeError):
            ler_csv(self.csv)

    def test_11_json_malformado(self):
        self.json.write_text(
            '{"nome": "João",}',
            encoding="utf-8"
        )
        with self.assertRaises(json.JSONDecodeError):
            ler_json(self.json)

    def test_12_json_estrutura_invalida(self):
        self.json.write_text(
            '{"nome": "João"}',
            encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            ler_json(self.json)

    def test_13_csv_vazio(self):
        self.csv.write_text("", encoding="utf-8")
        dados = ler_csv(self.csv)
        # Comportamento da versao atual: retorna lista vazia.
        self.assertEqual(dados, [])


if __name__ == "__main__":
    unittest.main()

