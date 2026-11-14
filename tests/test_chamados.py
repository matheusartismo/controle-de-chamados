import contextlib
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import main
from chamados import (
    abrir_chamado, atualizar_status, carregar_chamados, carregar_exemplos,
    exportar_csv, listar_chamados, salvar_chamados,
)


class TestControleDeChamados(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.pasta = Path(self.temporario.name)
        self.arquivo = self.pasta / "dados" / "chamados.json"

    def test_base_nova_comeca_vazia(self):
        self.assertEqual(carregar_chamados(self.arquivo), [])
        self.assertFalse(self.arquivo.exists())

    def test_chamados_continuam_disponiveis_depois_de_salvar_e_reabrir(self):
        chamados = []
        abrir_chamado(chamados, "  Ana  ", "  Impressora sem conexão  ", "Alta")
        abrir_chamado(chamados, "Bruno", "Acesso ao sistema", "Baixa")
        atualizar_status(chamados, 1, "Resolvido")
        salvar_chamados(chamados, self.arquivo)
        reabertos = carregar_chamados(self.arquivo)
        self.assertEqual(reabertos[0]["solicitante"], "Ana")
        self.assertEqual(reabertos[0]["assunto"], "Impressora sem conexão")
        self.assertEqual(reabertos[0]["status"], "Resolvido")
        novo = abrir_chamado(reabertos, "Carla", "Planilha", "Média")
        self.assertEqual(novo["id"], 3)

    def test_entrada_invalida_nao_cria_chamado(self):
        for solicitante, assunto, prioridade in [(" ", "Problema", "Alta"), ("Ana", " ", "Alta"), ("Ana", "Problema", "Urgente")]:
            with self.subTest(solicitante=solicitante, assunto=assunto, prioridade=prioridade):
                chamados = []
                with self.assertRaises(ValueError):
                    abrir_chamado(chamados, solicitante, assunto, prioridade)
                self.assertEqual(chamados, [])

    def test_filtro_mostra_apenas_status_escolhido_em_ordem_de_prioridade(self):
        chamados = []
        abrir_chamado(chamados, "Ana", "Baixa", "Baixa")
        abrir_chamado(chamados, "Bruno", "Alta", "Alta")
        abrir_chamado(chamados, "Carla", "Resolvido", "Média")
        atualizar_status(chamados, 3, "Resolvido")
        self.assertEqual([item["id"] for item in listar_chamados(chamados, "Aberto")], [2, 1])
        self.assertEqual(len(chamados), 3)

    def test_numero_inexistente_e_status_invalido_nao_alteram_chamados(self):
        chamados = []
        abrir_chamado(chamados, "Ana", "Problema", "Alta")
        antes = json.dumps(chamados)
        with self.assertRaises(ValueError):
            atualizar_status(chamados, 99, "Resolvido")
        with self.assertRaises(ValueError):
            atualizar_status(chamados, 1, "Desconhecido")
        self.assertEqual(json.dumps(chamados), antes)

    def test_csv_preserva_acentos_ponto_e_virgula_e_protege_textos_de_formula(self):
        chamados = []
        abrir_chamado(chamados, "=1+1", "Impressão; conexão", "Alta")
        destino = exportar_csv(chamados, self.pasta / "relatorio.csv")
        self.assertTrue(destino.read_bytes().startswith(b"\xef\xbb\xbf"))
        with destino.open(encoding="utf-8-sig", newline="") as arquivo:
            linhas = list(csv.reader(arquivo, delimiter=";"))
        self.assertEqual(linhas[1][1], "'=1+1")
        self.assertEqual(linhas[1][2], "Impressão; conexão")
        self.assertEqual(len(linhas[1]), len(linhas[0]))

    def test_arquivo_corrompido_nao_e_apagado_ou_tratado_como_base_vazia(self):
        self.arquivo.parent.mkdir(parents=True)
        self.arquivo.write_text("{arquivo incompleto", encoding="utf-8")
        antes = self.arquivo.read_bytes()
        with self.assertRaises(ValueError):
            carregar_chamados(self.arquivo)
        self.assertEqual(self.arquivo.read_bytes(), antes)

    def test_demonstracao_nao_substitui_chamados_existentes(self):
        chamados = []
        carregar_exemplos(chamados)
        antes = json.dumps(chamados)
        with self.assertRaises(ValueError):
            carregar_exemplos(chamados)
        self.assertEqual(json.dumps(chamados), antes)

    def test_identificadores_duplicados_no_arquivo_sao_rejeitados(self):
        chamados = []
        abrir_chamado(chamados, "Ana", "Pedido", "Alta")
        chamados.append(chamados[0].copy())
        salvar_chamados(chamados, self.arquivo)
        with self.assertRaises(ValueError):
            carregar_chamados(self.arquivo)

    def test_fluxo_completo_pelo_menu(self):
        respostas = ["5", "2", "1", "1", "Davi", "Monitor sem imagem", "3", "3", "4", "3", "4", "0"]
        saida = io.StringIO()
        with patch("builtins.input", side_effect=respostas), contextlib.redirect_stdout(saida):
            resultado = main(self.arquivo)
        self.assertEqual(resultado, 0)
        chamados = carregar_chamados(self.arquivo)
        self.assertEqual(len(chamados), 4)
        self.assertEqual(chamados[3]["status"], "Resolvido")
        self.assertIn("Chamado #004 aberto e salvo", saida.getvalue())
        self.assertEqual(len(list((self.arquivo.parent / "exportacoes").glob("*.csv"))), 1)


if __name__ == "__main__":
    unittest.main()
