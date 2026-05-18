"""
Testes de integração para o serviço ViaCEP.

Estes são testes de integração porque validam a comunicação real (ou simulada)
com a API externa ViaCEP, o tratamento do contrato da resposta JSON e os fluxos
de erro de ponta a ponta — não apenas lógica interna isolada.

Para executar APENAS os testes de integração:
    pytest tests/test_viacep_integration.py -v

Para pular os testes que fazem chamadas reais à API (útil em CI sem rede):
    pytest tests/test_viacep_integration.py -v -m "not live"
"""

import json
import urllib.error
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from src.viacep import (
    CEPInvalidoError,
    CEPNaoEncontradoError,
    ViaCEPError,
    _limpar_cep,
    consultar_cep,
    formatar_endereco,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def resposta_cep_valido():
    """Fixture com payload real do ViaCEP para o CEP 01310-100 (Av. Paulista)."""
    return {
        "cep": "01310-100",
        "logradouro": "Avenida Paulista",
        "complemento": "de 1 a 610 - lado par",
        "bairro": "Bela Vista",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107",
    }


@pytest.fixture
def resposta_cep_nao_encontrado():
    """Fixture com resposta de CEP inválido retornada pela API."""
    return {"erro": True}


def _mock_urlopen(payload: dict, status: int = 200):
    """Helper que cria um mock de urllib.request.urlopen."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(payload).encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


# ── Testes: _limpar_cep ───────────────────────────────────────────────────────

def test_limpar_cep_com_traco():
    assert _limpar_cep("01310-100") == "01310100"


def test_limpar_cep_sem_traco():
    assert _limpar_cep("01310100") == "01310100"


def test_limpar_cep_com_espacos():
    assert _limpar_cep("  01310 100  ") == "01310100"


def test_limpar_cep_curto_levanta_erro():
    with pytest.raises(CEPInvalidoError, match="inválido"):
        _limpar_cep("1234")


def test_limpar_cep_letras_levanta_erro():
    with pytest.raises(CEPInvalidoError, match="inválido"):
        _limpar_cep("ABCDE-FGH")


# ── Testes de integração: consultar_cep (com mock) ───────────────────────────

def test_consultar_cep_retorna_dados_corretos(resposta_cep_valido):
    """
    Integração: valida que consultar_cep desserializa corretamente
    a resposta JSON da API e retorna o dicionário esperado.
    """
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = _mock_urlopen(resposta_cep_valido)

        resultado = consultar_cep("01310-100")

    assert resultado["logradouro"] == "Avenida Paulista"
    assert resultado["localidade"] == "São Paulo"
    assert resultado["uf"] == "SP"
    assert resultado["cep"] == "01310-100"


def test_consultar_cep_formata_url_corretamente(resposta_cep_valido):
    """
    Integração: verifica que a URL enviada à API usa o CEP sem traço.
    """
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = _mock_urlopen(resposta_cep_valido)

        consultar_cep("01310-100")

        chamada = mock_open.call_args[0][0]
        assert "01310100" in chamada.full_url
        assert "viacep.com.br" in chamada.full_url


def test_consultar_cep_nao_encontrado_levanta_erro(resposta_cep_nao_encontrado):
    """
    Integração: valida que a flag {"erro": true} da API é convertida
    na exceção correta (CEPNaoEncontradoError).
    """
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.return_value = _mock_urlopen(resposta_cep_nao_encontrado)

        with pytest.raises(CEPNaoEncontradoError, match="não encontrado"):
            consultar_cep("99999999")


def test_consultar_cep_invalido_levanta_erro_antes_da_rede():
    """
    Integração: CEP com formato errado deve falhar antes de qualquer
    chamada de rede (não deve chamar urlopen).
    """
    with patch("urllib.request.urlopen") as mock_open:
        with pytest.raises(CEPInvalidoError):
            consultar_cep("123")
        mock_open.assert_not_called()


def test_consultar_cep_http_error_levanta_viacep_error():
    """
    Integração: erro HTTP da API (ex: 500) deve ser capturado e
    re-levantado como ViaCEPError.
    """
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.side_effect = urllib.error.HTTPError(
            url="https://viacep.com.br/ws/01310100/json/",
            code=500,
            msg="Internal Server Error",
            hdrs=None,
            fp=None,
        )

        with pytest.raises(ViaCEPError, match="Erro HTTP 500"):
            consultar_cep("01310100")


def test_consultar_cep_timeout_levanta_viacep_error():
    """
    Integração: falha de rede (timeout, sem conexão) deve ser capturada
    e re-levantada como ViaCEPError com mensagem descritiva.
    """
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.side_effect = urllib.error.URLError(reason="timed out")

        with pytest.raises(ViaCEPError, match="Falha de conexão"):
            consultar_cep("01310100")


def test_consultar_cep_json_invalido_levanta_viacep_error():
    """
    Integração: resposta com JSON malformado deve levantar ViaCEPError.
    """
    mock_response = MagicMock()
    mock_response.read.return_value = b"not-json{{{"
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_response):
        with pytest.raises(ViaCEPError, match="inválida"):
            consultar_cep("01310100")


# ── Testes: formatar_endereco ─────────────────────────────────────────────────

def test_formatar_endereco_completo(resposta_cep_valido):
    resultado = formatar_endereco(resposta_cep_valido)
    assert "Avenida Paulista" in resultado
    assert "Bela Vista" in resultado
    assert "São Paulo/SP" in resultado


def test_formatar_endereco_sem_logradouro():
    dados = {"localidade": "São Paulo", "uf": "SP", "bairro": "Centro"}
    resultado = formatar_endereco(dados)
    assert "São Paulo/SP" in resultado
    assert "Centro" in resultado


def test_formatar_endereco_vazio():
    resultado = formatar_endereco({})
    assert resultado == "Endereço não disponível"
