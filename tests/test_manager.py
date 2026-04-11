"""Testes automatizados para o módulo manager."""

import pytest
from src.manager import (
    adicionar_gasto,
    calcular_total,
    listar_gastos,
    remover_gasto,
    resumo_por_categoria,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def gastos_vazios():
    return []


@pytest.fixture
def gastos_populados():
    gastos = []
    adicionar_gasto(gastos, "Almoço", 35.00, "alimentação")
    adicionar_gasto(gastos, "Uber", 22.50, "transporte")
    adicionar_gasto(gastos, "Academia", 99.90, "saúde")
    return gastos


# ── Testes: adicionar_gasto ───────────────────────────────────────────────────

def test_adicionar_gasto_sucesso(gastos_vazios):
    gasto = adicionar_gasto(gastos_vazios, "Café", 8.50, "alimentação")
    assert gasto["descricao"] == "Café"
    assert gasto["valor"] == 8.50
    assert gasto["categoria"] == "alimentação"
    assert gasto["id"] == 1
    assert len(gastos_vazios) == 1


def test_adicionar_multiplos_ids_incrementais(gastos_vazios):
    adicionar_gasto(gastos_vazios, "Item 1", 10.0, "outros")
    adicionar_gasto(gastos_vazios, "Item 2", 20.0, "outros")
    adicionar_gasto(gastos_vazios, "Item 3", 30.0, "outros")
    ids = [g["id"] for g in gastos_vazios]
    assert ids == [1, 2, 3]


def test_adicionar_gasto_descricao_vazia(gastos_vazios):
    with pytest.raises(ValueError, match="descrição não pode ser vazia"):
        adicionar_gasto(gastos_vazios, "   ", 10.0, "outros")


def test_adicionar_gasto_valor_zero(gastos_vazios):
    with pytest.raises(ValueError, match="valor deve ser maior que zero"):
        adicionar_gasto(gastos_vazios, "Teste", 0.0, "outros")


def test_adicionar_gasto_valor_negativo(gastos_vazios):
    with pytest.raises(ValueError, match="valor deve ser maior que zero"):
        adicionar_gasto(gastos_vazios, "Teste", -5.0, "outros")


def test_adicionar_gasto_categoria_invalida(gastos_vazios):
    with pytest.raises(ValueError, match="Categoria inválida"):
        adicionar_gasto(gastos_vazios, "Teste", 10.0, "viagem")


# ── Testes: remover_gasto ─────────────────────────────────────────────────────

def test_remover_gasto_sucesso(gastos_populados):
    id_alvo = gastos_populados[0]["id"]
    removido = remover_gasto(gastos_populados, id_alvo)
    assert removido["id"] == id_alvo
    assert len(gastos_populados) == 2


def test_remover_gasto_id_inexistente(gastos_populados):
    with pytest.raises(ValueError, match="não encontrado"):
        remover_gasto(gastos_populados, 9999)


# ── Testes: listar_gastos ─────────────────────────────────────────────────────

def test_listar_todos(gastos_populados):
    lista = listar_gastos(gastos_populados)
    assert len(lista) == 3


def test_listar_com_filtro_categoria(gastos_populados):
    lista = listar_gastos(gastos_populados, "saúde")
    assert len(lista) == 1
    assert lista[0]["descricao"] == "Academia"


def test_listar_categoria_sem_resultados(gastos_populados):
    lista = listar_gastos(gastos_populados, "lazer")
    assert lista == []


def test_listar_gastos_vazios(gastos_vazios):
    assert listar_gastos(gastos_vazios) == []


# ── Testes: calcular_total ────────────────────────────────────────────────────

def test_calcular_total(gastos_populados):
    total = calcular_total(gastos_populados)
    assert total == pytest.approx(157.40)


def test_calcular_total_lista_vazia(gastos_vazios):
    assert calcular_total(gastos_vazios) == 0.0


# ── Testes: resumo_por_categoria ──────────────────────────────────────────────

def test_resumo_por_categoria(gastos_populados):
    resumo = resumo_por_categoria(gastos_populados)
    assert resumo["alimentação"] == pytest.approx(35.00)
    assert resumo["transporte"] == pytest.approx(22.50)
    assert resumo["saúde"] == pytest.approx(99.90)


def test_resumo_lista_vazia(gastos_vazios):
    assert resumo_por_categoria(gastos_vazios) == {}