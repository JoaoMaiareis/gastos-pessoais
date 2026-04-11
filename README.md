# 💰 Gerenciador de Gastos Pessoais

![CI](https://github.com/JoaoMaiareis/gastos-pessoais/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-yellow)

## Descrição do Problema

Muitas pessoas têm dificuldade em controlar seus gastos diários, o que leva ao
endividamento e à falta de planejamento financeiro. A ausência de uma ferramenta
simples e acessível faz com que pequenas despesas passem despercebidas ao longo do mês.

## Proposta da Solução

Uma aplicação de linha de comando (CLI) que permite registrar, visualizar e
analisar gastos pessoais por categoria, ajudando o usuário a entender para onde
seu dinheiro está indo de forma rápida e sem burocracia.

## Público-Alvo

Pessoas que desejam controlar suas finanças pessoais de forma simples, sem
depender de planilhas ou aplicativos complexos.

## Funcionalidades Principais

- ✅ Adicionar gastos com descrição, valor e categoria
- 📋 Listar todos os gastos (com filtro por categoria)
- 🗑️ Remover gastos pelo ID
- 📊 Ver resumo total e percentual por categoria
- 💾 Dados persistidos em arquivo JSON local

## Tecnologias Utilizadas

- **Python 3.11+** — linguagem principal
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)
- **JSON** — armazenamento local dos dados

---

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

---

## Execução

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
```

### Categorias disponíveis

`alimentação` | `transporte` | `saúde` | `lazer` | `educação` | `outros`

---

## Rodando os Testes

```bash
pytest --tb=short -v
```

---

## Rodando o Lint

```bash
ruff check .
```

---

## Versão Atual

**1.0.0** — versão inicial com funcionalidades CRUD e resumo por categoria.

---

## Autor

Joao Maia Reis
- GitHub: [@JoaoMaiareis](https://github.com/JoaoMaiareis)

## Repositório

[https://github.com/JoaoMaiareis/gastos-pessoais](https://github.com/JoaoMaiareis
/gastos-pessoais)
