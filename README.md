# Controle de chamados

Projeto de estudo de **Matheus Artismo**, estudante de **Análise e Desenvolvimento de Sistemas na Unisul**.

Um programa em Python para registrar pedidos de suporte e acompanhar o atendimento pelo terminal. A ideia é praticar programação usando uma situação comum em empresas: alguém informa um problema, a equipe identifica a prioridade e atualiza o andamento.

## Problema e exemplo de uso

Pedidos espalhados em mensagens podem perder informações importantes. Este projeto reúne solicitante, assunto, prioridade e status em uma lista local.

Exemplo fictício: o Financeiro informa uma impressora sem conexão. O pedido recebe prioridade alta, passa de **Aberto** para **Em andamento** e, depois do atendimento, para **Resolvido**. A lista pode ser exportada para análise em uma planilha.

## Funcionalidades implementadas

- Abrir chamados com número sequencial, solicitante, assunto e prioridade.
- Listar todos os chamados ou filtrar por status.
- Mostrar os chamados de prioridade alta primeiro.
- Atualizar o status e registrar a data da alteração.
- Salvar e reabrir os dados em um arquivo JSON.
- Exportar relatórios em CSV, com acentos e separador ponto e vírgula.
- Carregar três exemplos fictícios em uma base vazia.
- Validar entradas e preservar um arquivo de dados inválido para conferência.

## Como executar no Windows

Requisito: **Python 3.11 ou mais recente**, instalado a partir do [site oficial do Python](https://www.python.org/downloads/).

1. Baixe e extraia os arquivos do projeto.
2. Entre na pasta que contém `app.py`.
3. Dê dois cliques em `iniciar.bat`.

Também é possível abrir um terminal nessa pasta e executar:

```bash
py app.py
```

Se o comando `py` não estiver disponível, tente `python app.py`. Em Linux ou macOS, use `python3 app.py`.

**Não há bibliotecas externas para instalar.**

## Demonstração rápida

1. Na primeira execução, escolha **5 — Carregar exemplos fictícios**.
2. Escolha **2 — Listar chamados** e **1 — Todos**.
3. Abra um novo chamado pela opção **1**.
4. Pela opção **3**, informe o número desse chamado e selecione outro status.
5. Exporte pela opção **4** e abra o CSV gerado.
6. Saia pela opção **0**, abra o programa novamente e confira os dados.

O aplicativo cria `dados/chamados.json` depois da primeira gravação. As exportações ficam em `dados/exportacoes/`. Essas pastas contêm os dados locais de uso e estão no `.gitignore`.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `app.py` | Menu, perguntas e apresentação das informações. |
| `chamados.py` | Regras dos chamados, gravação e exportação. |
| `iniciar.bat` | Atalho para executar no Windows. |
| `tests/test_chamados.py` | Testes automatizados dos comportamentos principais. |
| `APRENDA.md` | Guia para estudar e modificar o código. |
| `PUBLICAR_NO_GITHUB.md` | Passo a passo para publicar o projeto. |

## Testes

Na pasta do projeto, execute:

```bash
py -m unittest discover -s tests -v
```

Os testes cobrem persistência após reabertura, entradas inválidas, filtros, atualização de status, exportação CSV, preservação de arquivos inválidos e um fluxo completo pelo menu. A verificação automatizada inicial foi executada com Python 3.12 em Linux. O atalho `iniciar.bat` deve ser conferido no Windows.

## Tecnologias e conceitos praticados

Python, funções, listas, dicionários, condições, laços, arquivos JSON, exportação CSV, tratamento de erros e testes com `unittest`.

Os textos que começam como fórmulas são tratados na exportação para evitar que sejam executados como fórmulas ao abrir uma planilha.

## Escopo desta versão

Aplicação local, para uma pessoa usando uma instância por vez. O arquivo JSON não implementa controle de acesso nem gravações simultâneas. Ainda não há interface gráfica, autenticação, SLA ou banco SQL.

## Próximas melhorias para desenvolver

- [ ] Pesquisar chamados pelo assunto.
- [ ] Acrescentar uma descrição detalhada do atendimento.
- [ ] Contar chamados por prioridade.
- [ ] Migrar o armazenamento para SQLite após estudar SQL.
- [ ] Criar uma interface gráfica ou web em uma etapa posterior.

## Aprendizagem e autoria

Projeto inicial preparado com apoio de IA para estudo. Meu objetivo é compreender o código, testar os comportamentos e registrar minhas próprias melhorias no histórico do repositório.

Perfil: [github.com/matheusartismo](https://github.com/matheusartismo).

## Referências

- [Documentação oficial do Python: JSON](https://docs.python.org/pt-br/3.12/library/json.html).
- [Documentação oficial do Python: CSV](https://docs.python.org/pt-br/3.12/library/csv.html).
- [Documentação oficial do Python: unittest](https://docs.python.org/pt-br/3.12/library/unittest.html).
