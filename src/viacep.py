"""Integração com a API pública ViaCEP para enriquecimento de dados de gastos."""

import urllib.error
import urllib.request
import json


VIACEP_BASE_URL = "https://viacep.com.br/ws/{cep}/json/"


class ViaCEPError(Exception):
    """Exceção base para erros da integração ViaCEP."""


class CEPNaoEncontradoError(ViaCEPError):
    """Levantada quando o CEP não existe ou não é encontrado."""


class CEPInvalidoError(ViaCEPError):
    """Levantada quando o formato do CEP é inválido."""


def _limpar_cep(cep: str) -> str:
    """Remove traços e espaços do CEP e valida o formato."""
    cep_limpo = cep.replace("-", "").replace(" ", "").strip()
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        raise CEPInvalidoError(
            f"CEP '{cep}' inválido. Use o formato 01310-100 ou 01310100."
        )
    return cep_limpo


def consultar_cep(cep: str, timeout: int = 5) -> dict:
    """
    Consulta um CEP na API ViaCEP e retorna os dados de endereço.

    Args:
        cep: CEP no formato '01310-100' ou '01310100'.
        timeout: Tempo máximo de espera pela resposta (segundos).

    Returns:
        Dicionário com logradouro, bairro, localidade, UF, etc.

    Raises:
        CEPInvalidoError: Se o formato do CEP for inválido.
        CEPNaoEncontradoError: Se o CEP não existir.
        ViaCEPError: Para outros erros de comunicação.
    """
    cep_limpo = _limpar_cep(cep)
    url = VIACEP_BASE_URL.format(cep=cep_limpo)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "gastos-pessoais/2.0 (github.com/JoaoMaiareis)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            dados = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ViaCEPError(f"Erro HTTP {exc.code} ao consultar ViaCEP.") from exc
    except urllib.error.URLError as exc:
        raise ViaCEPError(
            f"Falha de conexão com ViaCEP: {exc.reason}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ViaCEPError("Resposta inválida da API ViaCEP.") from exc

    # A API retorna {"erro": true} quando o CEP não é encontrado
    if dados.get("erro"):
        raise CEPNaoEncontradoError(f"CEP '{cep}' não encontrado.")

    return dados


def formatar_endereco(dados: dict) -> str:
    """
    Formata os dados do ViaCEP em uma string legível.

    Args:
        dados: Dicionário retornado por consultar_cep().

    Returns:
        String formatada com o endereço completo.
    """
    partes = []
    if dados.get("logradouro"):
        partes.append(dados["logradouro"])
    if dados.get("bairro"):
        partes.append(dados["bairro"])
    if dados.get("localidade") and dados.get("uf"):
        partes.append(f"{dados['localidade']}/{dados['uf']}")
    elif dados.get("localidade"):
        partes.append(dados["localidade"])
    return " — ".join(partes) if partes else "Endereço não disponível"
