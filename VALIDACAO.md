# Verificação da versão inicial

Data: 14 de novembro de 2026.

Ambiente utilizado: Python 3.12.14, Linux.

Comando executado na pasta do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Resultado: **10 testes executados, todos passaram**.

| Comportamento verificado | Resultado |
| --- | --- |
| Começar com uma base nova vazia | Passou |
| Salvar, reabrir e continuar a numeração | Passou |
| Recusar entradas obrigatórias vazias e prioridade inválida | Passou |
| Filtrar status e ordenar prioridade | Passou |
| Recusar número inexistente e status inválido | Passou |
| Exportar CSV com acentos, separador e proteção de fórmulas | Passou |
| Preservar arquivo corrompido para conferência | Passou |
| Impedir que exemplos substituam dados existentes | Passou |
| Recusar identificadores duplicados em arquivo | Passou |
| Abrir, listar, atualizar e exportar pelo menu | Passou |

O fluxo do menu foi automatizado com entradas simuladas e arquivos temporários. O atalho `iniciar.bat` não foi executado em Windows neste ambiente; faça essa conferência no seu computador.
