"""Módulo principal de gerenciamento de gastos pessoais."""

import json
import os
from datetime import datetime

CATEGORIAS_VALIDAS = [
    "alimentação",
    "transporte",
    "saúde",
    "lazer",
    "educação",
    "outros",
]


def carregar_dados(caminho: str) -> list[dict]:
    """Carrega os gastos salvos no arquivo JSON."""
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(caminho: str, gastos: list[dict]) -> None:
    """Salva os gastos no arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(gastos, f, ensure_ascii=False, indent=2)


def adicionar_gasto(
    gastos: list[dict],
    descricao: str,
    valor: float,
    categoria: str,
) -> dict:
    """Adiciona um novo gasto à lista. Retorna o gasto criado."""
    if not descricao or not descricao.strip():
        raise ValueError("A descrição não pode ser vazia.")
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    categoria = categoria.lower().strip()
    if categoria not in CATEGORIAS_VALIDAS:
        raise ValueError(
            f"Categoria inválida. Escolha entre: {', '.join(CATEGORIAS_VALIDAS)}"
        )

    novo_id = max((g["id"] for g in gastos), default=0) + 1
    gasto = {
        "id": novo_id,
        "descricao": descricao.strip(),
        "valor": round(valor, 2),
        "categoria": categoria,
        "data": datetime.now().strftime("%Y-%m-%d"),
    }
    gastos.append(gasto)
    return gasto


def remover_gasto(gastos: list[dict], gasto_id: int) -> dict:
    """Remove um gasto pelo ID. Retorna o gasto removido."""
    for i, gasto in enumerate(gastos):
        if gasto["id"] == gasto_id:
            return gastos.pop(i)
    raise ValueError(f"Gasto com ID {gasto_id} não encontrado.")


def listar_gastos(gastos: list[dict], categoria: str | None = None) -> list[dict]:
    """Retorna todos os gastos, com filtro opcional por categoria."""
    if categoria:
        return [g for g in gastos if g["categoria"] == categoria.lower().strip()]
    return list(gastos)


def calcular_total(gastos: list[dict]) -> float:
    """Calcula a soma total dos gastos."""
    return round(sum(g["valor"] for g in gastos), 2)


def resumo_por_categoria(gastos: list[dict]) -> dict[str, float]:
    """Retorna o total gasto por categoria."""
    resumo: dict[str, float] = {}
    for gasto in gastos:
        cat = gasto["categoria"]
        resumo[cat] = round(resumo.get(cat, 0) + gasto["valor"], 2)
    return resumo
