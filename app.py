"""Execute este arquivo para usar o sistema pelo terminal."""

from datetime import datetime
from pathlib import Path

from chamados import (
    PRIORIDADES, STATUS, abrir_chamado, atualizar_status, carregar_chamados,
    carregar_exemplos, exportar_csv, listar_chamados, salvar_chamados,
)

ARQUIVO_DADOS = Path(__file__).resolve().parent / "dados" / "chamados.json"


def escolher(titulo, opcoes):
    print("\n" + titulo)
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"{numero}. {opcao}")
    print("0. Voltar")
    while True:
        resposta = input("Escolha: ").strip()
        if resposta == "0":
            return None
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return opcoes[int(resposta) - 1]
        print("Digite um dos números do menu.")


def mostrar_chamados(chamados):
    if not chamados:
        print("\nNenhum chamado encontrado.")
        return
    for chamado in chamados:
        print(f"\nChamado #{chamado['id']:03d} | {chamado['prioridade']} | {chamado['status']}")
        print(f"Solicitante: {chamado['solicitante']}")
        print(f"Assunto: {chamado['assunto']}")
        print(f"Criado em: {chamado['criado_em'].replace('T', ' ')}")


def main(arquivo=ARQUIVO_DADOS):
    arquivo = Path(arquivo)
    try:
        chamados = carregar_chamados(arquivo)
    except (ValueError, OSError) as erro:
        print(f"Não foi possível abrir os chamados: {erro}")
        return 1

    print("CONTROLE DE CHAMADOS — Projeto de estudo de Matheus Artismo")
    try:
        while True:
            print("\nResumo: " + " | ".join(
                f"{status}: {sum(chamado['status'] == status for chamado in chamados)}"
                for status in STATUS
            ))
            print("\n1. Abrir chamado\n2. Listar chamados\n3. Atualizar status")
            print("4. Exportar para CSV\n5. Carregar exemplos fictícios\n0. Sair")
            opcao = input("Escolha: ").strip()

            try:
                if opcao == "0":
                    print("Até mais!")
                    return 0

                elif opcao == "1":
                    solicitante = input("Nome ou setor de quem solicitou: ")
                    assunto = input("Qual é o problema ou pedido? ")
                    prioridade = escolher("Prioridade do chamado", PRIORIDADES)
                    if prioridade is None:
                        continue
                    chamado = abrir_chamado(chamados, solicitante, assunto, prioridade)
                    salvar_chamados(chamados, arquivo)
                    print(f"Chamado #{chamado['id']:03d} aberto e salvo.")

                elif opcao == "2":
                    filtro = escolher("Filtrar por status", ("Todos",) + STATUS)
                    if filtro is not None:
                        mostrar_chamados(listar_chamados(chamados, None if filtro == "Todos" else filtro))

                elif opcao == "3":
                    resposta = input("Número do chamado: ").strip()
                    if not resposta.isdigit() or int(resposta) < 1:
                        raise ValueError("Digite o número positivo do chamado, como 1 ou 2.")
                    novo_status = escolher("Novo status", STATUS)
                    if novo_status is None:
                        continue
                    chamado = atualizar_status(chamados, int(resposta), novo_status)
                    salvar_chamados(chamados, arquivo)
                    print(f"Chamado #{chamado['id']:03d} atualizado para {novo_status} e salvo.")

                elif opcao == "4":
                    if not chamados:
                        print("Cadastre um chamado antes de exportar.")
                        continue
                    nome = "chamados_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".csv"
                    destino = exportar_csv(chamados, arquivo.parent / "exportacoes" / nome)
                    print(f"Planilha criada: {destino}")

                elif opcao == "5":
                    carregar_exemplos(chamados)
                    salvar_chamados(chamados, arquivo)
                    print("Três chamados fictícios foram carregados e salvos.")

                else:
                    print("Digite um dos números do menu.")

            except ValueError as erro:
                print(f"Atenção: {erro}")

    except OSError as erro:
        print(f"Não foi possível ler ou gravar o arquivo: {erro}")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
