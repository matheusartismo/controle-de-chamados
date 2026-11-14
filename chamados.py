"""Regras e arquivos do controle de chamados. Não abre o menu ao importar."""

import csv
import json
from datetime import datetime
from pathlib import Path

PRIORIDADES = ("Baixa", "Média", "Alta")
STATUS = ("Aberto", "Em andamento", "Resolvido")


def agora():
    return datetime.now().isoformat(timespec="seconds")


def carregar_chamados(arquivo):
    """Uma base nova começa vazia. Um arquivo inválido nunca vira uma base vazia."""
    arquivo = Path(arquivo)
    if not arquivo.exists():
        return []
    try:
        chamados = json.loads(arquivo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise ValueError("O arquivo de chamados está inválido. Confira-o antes de continuar.") from erro

    campos = {"id", "solicitante", "assunto", "prioridade", "status", "criado_em", "atualizado_em"}
    if not isinstance(chamados, list):
        raise ValueError("O arquivo precisa conter uma lista de chamados.")
    ids = set()
    for chamado in chamados:
        if not isinstance(chamado, dict) or not campos.issubset(chamado):
            raise ValueError("Há um chamado com campos ausentes no arquivo.")
        identificador = chamado["id"]
        if type(identificador) is not int or identificador < 1 or identificador in ids:
            raise ValueError("Os números dos chamados precisam ser positivos e únicos.")
        ids.add(identificador)
        if any(not isinstance(chamado[campo], str) for campo in campos - {"id"}):
            raise ValueError("Há um chamado com textos inválidos no arquivo.")
        if not chamado["solicitante"].strip() or not chamado["assunto"].strip():
            raise ValueError("Há um chamado sem solicitante ou assunto.")
        if chamado["prioridade"] not in PRIORIDADES or chamado["status"] not in STATUS:
            raise ValueError("Há uma prioridade ou um status inválido no arquivo.")
    return chamados


def salvar_chamados(chamados, arquivo):
    """Grava primeiro um arquivo temporário para reduzir o risco de gravação incompleta."""
    arquivo = Path(arquivo)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    temporario = arquivo.with_suffix(arquivo.suffix + ".tmp")
    texto = json.dumps(chamados, ensure_ascii=False, indent=2)
    temporario.write_text(texto + "\n", encoding="utf-8")
    temporario.replace(arquivo)


def abrir_chamado(chamados, solicitante, assunto, prioridade):
    solicitante = solicitante.strip()
    assunto = assunto.strip()
    if not solicitante or not assunto:
        raise ValueError("Preencha o solicitante e o assunto.")
    if len(solicitante) > 80 or len(assunto) > 160:
        raise ValueError("Use até 80 caracteres no solicitante e 160 no assunto.")
    if prioridade not in PRIORIDADES:
        raise ValueError("Escolha uma prioridade válida.")

    identificador = max((chamado["id"] for chamado in chamados), default=0) + 1
    data = agora()
    chamado = {
        "id": identificador,
        "solicitante": solicitante,
        "assunto": assunto,
        "prioridade": prioridade,
        "status": "Aberto",
        "criado_em": data,
        "atualizado_em": data,
    }
    chamados.append(chamado)
    return chamado


def listar_chamados(chamados, status=None):
    if status is not None and status not in STATUS:
        raise ValueError("Escolha um status válido.")
    selecionados = [chamado for chamado in chamados if status is None or chamado["status"] == status]
    ordem = {"Alta": 0, "Média": 1, "Baixa": 2}
    return sorted(selecionados, key=lambda chamado: (ordem[chamado["prioridade"]], chamado["id"]))


def atualizar_status(chamados, identificador, novo_status):
    if novo_status not in STATUS:
        raise ValueError("Escolha um status válido.")
    for chamado in chamados:
        if chamado["id"] == identificador:
            chamado["status"] = novo_status
            chamado["atualizado_em"] = agora()
            return chamado
    raise ValueError("Não foi encontrado um chamado com esse número.")


def texto_para_planilha(valor):
    """Evita que textos de usuário sejam interpretados como fórmulas no Excel."""
    texto = str(valor)
    if texto.lstrip().startswith(("=", "+", "-", "@")) or texto.startswith(("\t", "\r", "\n")):
        return "'" + texto
    return texto


def exportar_csv(chamados, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Ponto e vírgula e UTF-8 com BOM facilitam a abertura no Excel em português.
    with destino.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["Número", "Solicitante", "Assunto", "Prioridade", "Status", "Criado em", "Atualizado em"])
        for chamado in listar_chamados(chamados):
            linha = [chamado[campo] for campo in ("id", "solicitante", "assunto", "prioridade", "status", "criado_em", "atualizado_em")]
            escritor.writerow([texto_para_planilha(valor) for valor in linha])
    return destino


def carregar_exemplos(chamados):
    """A demonstração usa pessoas e problemas fictícios e só entra numa base vazia."""
    if chamados:
        raise ValueError("Os exemplos só podem ser carregados quando a lista está vazia.")
    abrir_chamado(chamados, "Ana — Financeiro", "Impressora sem conexão", "Alta")
    abrir_chamado(chamados, "Bruno — Comercial", "Planilha não abre", "Média")
    abrir_chamado(chamados, "Carla — RH", "Solicitação de acesso ao sistema", "Baixa")
    atualizar_status(chamados, 1, "Em andamento")
    atualizar_status(chamados, 3, "Resolvido")
