"""Interface de linha de comando para o Gerenciador de Gastos Pessoais."""

import argparse
import sys

from src.manager import (
    CATEGORIAS_VALIDAS,
    adicionar_gasto,
    calcular_total,
    carregar_dados,
    listar_gastos,
    remover_gasto,
    resumo_por_categoria,
    salvar_dados,
)
from src.viacep import (
    CEPInvalidoError,
    CEPNaoEncontradoError,
    ViaCEPError,
    consultar_cep,
    formatar_endereco,
)

ARQUIVO_DADOS = "gastos.json"


def cmd_adicionar(args: argparse.Namespace) -> None:
    gastos = carregar_dados(ARQUIVO_DADOS)
    try:
        gasto = adicionar_gasto(gastos, args.descricao, args.valor, args.categoria)
        salvar_dados(ARQUIVO_DADOS, gastos)
        print(
            f"✅ Gasto adicionado: [#{gasto['id']}] {gasto['descricao']} "
            f"- R$ {gasto['valor']:.2f} ({gasto['categoria']}) em {gasto['data']}"
        )
    except ValueError as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


def cmd_listar(args: argparse.Namespace) -> None:
    gastos = carregar_dados(ARQUIVO_DADOS)
    lista = listar_gastos(gastos, getattr(args, "categoria", None))
    if not lista:
        print("📭 Nenhum gasto encontrado.")
        return
    print(f"\n{'ID':<5} {'Data':<12} {'Categoria':<14} {'Valor':>10}  Descrição")
    print("-" * 65)
    for g in lista:
        print(
            f"{g['id']:<5} {g['data']:<12} {g['categoria']:<14} "
            f"R$ {g['valor']:>7.2f}  {g['descricao']}"
        )
    print("-" * 65)
    print(f"{'TOTAL':>33} R$ {calcular_total(lista):>7.2f}\n")


def cmd_remover(args: argparse.Namespace) -> None:
    gastos = carregar_dados(ARQUIVO_DADOS)
    try:
        gasto = remover_gasto(gastos, args.id)
        salvar_dados(ARQUIVO_DADOS, gastos)
        print(f"🗑️  Gasto removido: [#{gasto['id']}] {gasto['descricao']}")
    except ValueError as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


def cmd_resumo(_args: argparse.Namespace) -> None:
    gastos = carregar_dados(ARQUIVO_DADOS)
    if not gastos:
        print("📭 Nenhum gasto registrado ainda.")
        return
    resumo = resumo_por_categoria(gastos)
    total = calcular_total(gastos)
    print("\n📊 Resumo por categoria:")
    print("-" * 35)
    for cat, valor in sorted(resumo.items(), key=lambda x: -x[1]):
        pct = (valor / total) * 100 if total else 0
        print(f"  {cat:<14}  R$ {valor:>8.2f}  ({pct:.1f}%)")
    print("-" * 35)
    print(f"  {'TOTAL':<14}  R$ {total:>8.2f}\n")


def cmd_cep(args: argparse.Namespace) -> None:
    """Consulta um CEP na API ViaCEP e exibe o endereço correspondente."""
    print(f"🔍 Consultando CEP {args.cep}...")
    try:
        dados = consultar_cep(args.cep)
        print(f"\n📍 Endereço encontrado:")
        print(f"   CEP:          {dados.get('cep', '-')}")
        print(f"   Logradouro:   {dados.get('logradouro', '-')}")
        print(f"   Complemento:  {dados.get('complemento', '-') or '-'}")
        print(f"   Bairro:       {dados.get('bairro', '-')}")
        print(f"   Cidade/UF:    {dados.get('localidade', '-')}/{dados.get('uf', '-')}")
        print(f"   DDD:          {dados.get('ddd', '-')}")
        print(f"\n   ↳ {formatar_endereco(dados)}\n")
    except CEPInvalidoError as e:
        print(f"❌ CEP inválido: {e}")
        sys.exit(1)
    except CEPNaoEncontradoError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ViaCEPError as e:
        print(f"❌ Erro ao consultar API: {e}")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gastos",
        description="💰 Gerenciador de Gastos Pessoais",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # adicionar
    p_add = subparsers.add_parser("adicionar", help="Registrar um novo gasto")
    p_add.add_argument("descricao", type=str, help="Descrição do gasto")
    p_add.add_argument("valor", type=float, help="Valor em reais (ex: 35.90)")
    p_add.add_argument(
        "categoria",
        choices=CATEGORIAS_VALIDAS,
        help="Categoria do gasto",
    )
    p_add.set_defaults(func=cmd_adicionar)

    # listar
    p_list = subparsers.add_parser("listar", help="Listar todos os gastos")
    p_list.add_argument(
        "--categoria",
        choices=CATEGORIAS_VALIDAS,
        help="Filtrar por categoria",
    )
    p_list.set_defaults(func=cmd_listar)

    # remover
    p_rm = subparsers.add_parser("remover", help="Remover um gasto pelo ID")
    p_rm.add_argument("id", type=int, help="ID do gasto a remover")
    p_rm.set_defaults(func=cmd_remover)

    # resumo
    p_res = subparsers.add_parser("resumo", help="Ver resumo por categoria")
    p_res.set_defaults(func=cmd_resumo)

    # cep
    p_cep = subparsers.add_parser("cep", help="Consultar endereço por CEP (ViaCEP)")
    p_cep.add_argument("cep", type=str, help="CEP a consultar (ex: 01310-100)")
    p_cep.set_defaults(func=cmd_cep)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
