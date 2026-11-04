# TED 03 – Gerenciador de Persistência de Dados (CSV e JSON)

**Instituição:** UniBalsas Centro Universitário  
**Curso:** Análise e Desenvolvimento de Sistemas (ADS)  
**Disciplina:** Algoritmos e Programação Avançada.  
**Autor (trabalho individual):** Vinicius Muniz Lopes dos Santos — R.A. 26.1.14496.

## Objetivo

Aplicação em Python, apenas com a biblioteca padrão, para leitura, escrita e conversão de CSV e JSON, tratamento de exceções e backup automático antes de sobrescrever arquivos existentes.

## Arquivos

- `main.py`: menu interativo e opções de demonstração.
- `config.py`: caminhos e codificações.
- `leitor.py`: lê e valida CSV e JSON.
- `escritor.py`: grava CSV/JSON e solicita backup antes de sobrescrever.
- `conversor.py`: converte dados de clientes entre formatos.
- `backup.py`: protege os dados antes de alterações.
- `erros.py`: apresenta mensagens amigáveis e recupera erros previstos.
- `dados/`: exemplos CSV e JSON.
- `dados/erros/`: arquivos para testar erros.
- `testes/test_persistencia.py`: 13 testes automatizados com `unittest`.
- `backups/`: criada automaticamente quando um arquivo existente é sobrescrito.

## Como executar

Requisito: Python 3.8+ (sem dependências externas).

```bash
python main.py
```

Também é possível executar uma opção diretamente, por exemplo:

```bash
python main.py 1
```

Opções: 1 = CSV para JSON; 2 = JSON para CSV; 3 = adicionar cliente com backup; 4 = arquivo inexistente; 5 = JSON malformado; 6 = codificação inválida; 7 = listar backups; 8 = exibir CSV; 0 = sair.

## Testes

```bash
python -m unittest discover -s testes -v
```

Os testes trabalham em pastas temporárias e incluem conversões, ida e volta, acentos, backups e erros. Capture os resultados reais no terminal para incluir como evidência no relatório.

## Limites e segurança

- Leitura: UTF-8 com aceitação de BOM. Escrita: UTF-8.
- `with open(...)` é usado nas leituras e escritas diretas do projeto.
- Os campos `id` e `valor` dos dados demonstrativos podem ser convertidos para inteiro e número decimal. O campo `valor` numérico é formatado com duas casas ao voltar para CSV. **Isto não garante preservação exata de qualquer texto numérico arbitrário** (como `001.2300`); a aplicação demonstrativa trabalha com valores monetários de duas casas.
- O backup do arquivo anterior é feito antes da escrita. Em caso de falha ao criar o backup, a operação é cancelada. O sistema não implementa transações atômicas completas contra falhas durante a escrita.
- Não publique dados pessoais reais em arquivos de exemplo.

## Entrega

Disponibilizar o código, os dados de demonstração, este README e o relatório técnico em PDF no repositório. Conferir o relatório para corresponder à versão testada e entregar o link do GitHub no Portal do Aluno. A atividade prevê dupla; verificar com o professor a autorização para entrega individual.
