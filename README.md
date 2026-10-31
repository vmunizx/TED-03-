# TED-03 - Gerenciador de Persistência de Dados (CSV e JSON)

**Instituição:** UniBalsas Centro Universitário
**Curso:** Análise e Desenvolvimento de Sistemas (ADS)
**Disciplina:** ALGORITMOS E PROGRAMAÇÃO AVANÇADA

## Autor

- Vinicius Muniz

## Descrição

Módulo em Python que gerencia dados persistidos em arquivos CSV e JSON, com
conversão entre os dois formatos, tratamento de erros de entrada/saída e
backup automático antes de qualquer alteração em arquivos existentes.
Usa apenas a biblioteca padrão (`csv`, `json`, `os`, `shutil`, `datetime`).

## Funcionalidades

- Leitura de CSV (`csv.DictReader`) e de JSON (`json.load`).
- Conversão CSV -> JSON e JSON -> CSV, preservando registros e valores.
- Escrita de CSV e JSON em UTF-8, com acentos preservados.
- Uso de `with open(..., encoding=...)` em todas as aberturas de arquivo.
- Backup automático com data e hora na pasta `backups/` antes de sobrescrever um arquivo.
  Se o backup falhar, nada é gravado.
- Tratamento de `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`,
  `json.JSONDecodeError` e `csv.Error`, com mensagens claras e sem encerrar o programa.
- Menu interativo com opções que demonstram cada cenário, inclusive os de erro.

## Estrutura do projeto

```
TED03_Persistencia/
├── main.py         # menu interativo
├── config.py       # caminhos do projeto
├── leitor.py       # leitura de CSV e JSON
├── escritor.py     # escrita de CSV e JSON (chama o backup antes)
├── conversor.py    # conversão CSV <-> JSON
├── backup.py       # backup automático
├── dados/
│   ├── clientes.csv
│   ├── clientes.json
│   └── erros/      # arquivos usados para testar erros
│       ├── malformado.json
│       └── latin1.csv
├── backups/        # criada automaticamente
└── README.md
```

## Como executar

Requisito: Python 3.8 ou superior.

```
python main.py
```

(em alguns sistemas, `python3 main.py`)

## Como testar

| Opção | O que faz | Resultado esperado |
|-------|-----------|--------------------|
| 1 | CSV -> JSON | Gera `dados/clientes_convertido.json` |
| 2 | JSON -> CSV | Gera `dados/clientes_convertido.csv` |
| 3 | Adiciona um cliente em `clientes.csv` | Mostra a mensagem de backup e cria o arquivo em `backups/` |
| 4 | Lê um arquivo que não existe | Mensagem de arquivo não encontrado |
| 5 | Lê um JSON malformado | Mensagem de JSON malformado, com linha e coluna |
| 6 | Lê um CSV em Latin-1 | Mensagem de erro de codificação |

## Observações

- O CSV guarda tudo como texto. Na conversão para JSON, `id` vira inteiro e
  `valor` vira número; se algum campo não puder ser convertido, ele é mantido como texto.
  Ao voltar para CSV, o valor numérico é preservado, mas zeros à direita podem
  mudar de aparência (`150.50` -> `150.5`).
- A leitura usa `utf-8-sig`, que é UTF-8 e também aceita o BOM que o Excel
  adiciona aos CSVs. A escrita usa UTF-8 puro.
