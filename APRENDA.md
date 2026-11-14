# Aprenda o projeto por partes

Você não precisa entender tudo de uma vez. Primeiro use o programa; depois abra uma função por vez no editor.

## 1. Faça o caminho de um chamado

Execute `app.py`, abra um chamado fictício, liste, altere o status, saia e abra de novo. Observe quais informações continuam disponíveis. Abra o arquivo `dados/chamados.json` para ver como os registros foram guardados.

## 2. Entenda cinco conceitos

| Conceito | Exemplo no projeto | Explicação simples |
| --- | --- | --- |
| Variável | `assunto` | Um nome usado para guardar um valor. |
| Lista | `chamados` | Um conjunto ordenado de registros. |
| Dicionário | Um registro com `id`, `assunto` e `status` | Um conjunto de campos com nome e valor. |
| Condição | `if opcao == "1"` | Decide o que o programa vai fazer. |
| Laço | `for chamado in chamados` | Percorre os registros um por um. |

## 3. Leia `abrir_chamado` em `chamados.py`

Essa função recebe a lista, o solicitante, o assunto e a prioridade. Ela remove espaços extras, confere os dados, calcula um número novo, monta um dicionário e acrescenta o registro à lista.

`return chamado` devolve o registro criado para o menu mostrar seu número. A gravação é uma etapa separada: `salvar_chamados` transforma a lista em texto JSON e grava o arquivo.

Pergunta para investigar no código: o que acontece se o solicitante estiver vazio? Execute esse caso e encontre a condição responsável.

## 4. Siga as outras funções

- `listar_chamados`: seleciona os registros e organiza por prioridade.
- `atualizar_status`: procura um número e altera o registro correspondente.
- `carregar_chamados`: lê os registros salvos e confere sua estrutura.
- `exportar_csv`: transforma os registros em linhas de uma planilha.

Depois, veja como `app.py` chama cada uma dessas funções ao receber um número do menu.

## 5. Faça uma primeira alteração sua

Comece mudando os textos do menu. Execute outra vez e confirme o resultado. Faça um commit com uma mensagem que descreva exatamente a mudança.

Em seguida, acrescente uma **contagem por prioridade** no resumo. Tente localizar como a contagem por status já foi feita e adapte a ideia. Confira com a base fictícia: há um chamado em cada prioridade.

Uma melhoria seguinte é pesquisar pelo assunto. Pense em quatro situações: busca com resultado, sem resultado, texto vazio e diferenças entre letras maiúsculas e minúsculas.

## 6. Use os testes para conferir as mudanças

Execute `py -m unittest discover -s tests -v` antes e depois de alterar as regras. Leia os nomes dos testes: eles descrevem comportamentos que precisam continuar funcionando. Ao implementar uma funcionalidade nova, acrescente um teste do seu comportamento.

## 7. Apresente o que você realmente compreendeu

Prepare uma demonstração curta: problema que o projeto resolve, abertura de um chamado, mudança de status e arquivo exportado. Explique uma função com suas palavras e mostre uma melhoria que você mesmo fez.

Descreva o projeto como estudo com apoio de IA e registre o que foi sua contribuição. Acrescente conhecimentos ao currículo conforme conseguir explicar e modificar essas partes.
