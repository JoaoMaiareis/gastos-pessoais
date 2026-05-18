# Gerenciador de Gastos Pessoais

![CI](https://github.com/JoaoMaiareis/gastos-pessoais/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-yellow)
![API](https://img.shields.io/badge/API-ViaCEP-green)

## Descrição do Projeto

Aplicação de linha de comando (CLI) para registro, visualização e análise de gastos pessoais por categoria. Na versão 2.0, o sistema integra-se com a API pública **ViaCEP** para consulta de endereços por CEP diretamente no terminal.

## Problema Resolvido

Muitas pessoas têm dificuldade em controlar seus gastos diários, o que leva ao endividamento e à falta de planejamento financeiro. Esta ferramenta simples e acessível registra despesas sem burocracia e ainda permite consultar o endereço de qualquer CEP brasileiro, útil ao registrar gastos de estabelecimentos.

## Funcionalidades

- ✅ Adicionar gastos com descrição, valor e categoria
- 📋 Listar todos os gastos (com filtro por categoria)
- 🗑️ Remover gastos pelo ID
- 📊 Ver resumo total e percentual por categoria
- 🔍 Consultar endereço por CEP via API ViaCEP *(novo na v2.0)*
- 💾 Dados persistidos em arquivo JSON local

## API Integrada — ViaCEP

A [ViaCEP](https://viacep.com.br) é uma API pública e gratuita que retorna dados de endereço para qualquer CEP válido do Brasil. Foi escolhida por:

- Ser 100% gratuita, sem necessidade de chave de API
- Ter documentação clara e resposta JSON padronizada
- Agregar valor real: ao registrar um gasto em um local, o usuário pode confirmar o endereço pelo CEP

**Endpoint utilizado:** `GET https://viacep.com.br/ws/{cep}/json/`

**Exemplo de resposta:**
```json
{
  "cep": "01310-100",
  "logradouro": "Avenida Paulista",
  "bairro": "Bela Vista",
  "localidade": "São Paulo",
  "uf": "SP",
  "ddd": "11"
}
```

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| pytest | Testes unitários e de integração |
| ruff | Linting e análise estática |
| GitHub Actions | CI/CD automatizado |
| ViaCEP API | Consulta de endereços por CEP |
| JSON | Armazenamento local dos dados |

## Estrutura do Projeto

```
gastos-pessoais/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline CI/CD
├── src/
│   ├── __init__.py
│   ├── manager.py          # Lógica de negócio dos gastos
│   └── viacep.py           # Integração com API ViaCEP (novo)
├── tests/
│   ├── __init__.py
│   ├── test_manager.py     # Testes unitários
│   └── test_viacep_integration.py  # Testes de integração (novo)
├── main.py                 # CLI — ponto de entrada
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/JoaoMaiareis/gastos-pessoais.git
cd gastos-pessoais

# 2. (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

## Como Executar

```bash
# Adicionar um gasto
python main.py adicionar "Almoço no restaurante" 35.90 alimentação

# Listar todos os gastos
python main.py listar

# Listar por categoria
python main.py listar --categoria transporte

# Ver resumo por categoria
python main.py resumo

# Remover um gasto pelo ID
python main.py remover 2

# Consultar endereço por CEP (novo!)
python main.py cep 01310-100
```

### Categorias disponíveis

`alimentação` | `transporte` | `saúde` | `lazer` | `educação` | `outros`

## Rodando os Testes

```bash
# Todos os testes
pytest --tb=short -v

# Apenas testes unitários
pytest tests/test_manager.py -v

# Apenas testes de integração (ViaCEP)
pytest tests/test_viacep_integration.py -v
```

## Rodando o Lint

```bash
ruff check .
```

## CI/CD

O projeto usa **GitHub Actions** com pipeline que executa automaticamente a cada push ou pull request na branch `main`:

1. Checkout do código
2. Configuração do Python 3.11
3. Instalação das dependências
4. Lint com `ruff`
5. Testes unitários com `pytest`
6. Testes de integração com `pytest`

## Deploy

O projeto é uma CLI Python, sem servidor web. O "deploy" acontece via GitHub Releases:

- [Releases](https://github.com/JoaoMaiareis/gastos-pessoais/releases) — versões estáveis para download
- Usuários fazem `git clone` ou baixam o ZIP da release e executam localmente

Para distribuição como pacote instalável:

```bash
pip install git+https://github.com/JoaoMaiareis/gastos-pessoais.git
gastos --help
```

## Versões

| Versão | Descrição |
|---|---|
| 2.0.0 | Integração ViaCEP, testes de integração, CI/CD atualizado |
| 1.0.0 | Versão inicial com CRUD de gastos |

## Autor

**Joao Maia Reis**
- GitHub: [@JoaoMaiareis](https://github.com/JoaoMaiareis)

## Repositório

[https://github.com/JoaoMaiareis/gastos-pessoais](https://github.com/JoaoMaiareis/gastos-pessoais)
