# URL Shortener

> Encurtador de URLs construído em Python + FastAPI, como projeto de portfólio para consolidar conceitos de engenharia de software, arquitetura de sistemas e boas práticas de backend.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![pytest](https://img.shields.io/badge/tests-6%20passed-brightgreen)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## Sobre o Projeto

Este projeto tem como objetivo implementar um **encurtador de URLs completo**, indo além do básico "gera código curto e redireciona". O foco é aplicar, na prática, decisões de arquitetura e engenharia que separam um projeto de estudo de um sistema real.

A base teórica vem de pesquisa própria sobre:
- Algoritmos de geração de chaves (Base62 vs. hashing vs. contador incremental)
- Status codes HTTP (301 vs. 302) e seu impacto em métricas e cache
- Segurança contra SSRF, spam e abuso de rate limit
- Estratégias de cache, escalabilidade e consistência

## Funcionalidades (implementadas)

- [x] Encurtamento de URL longa em código curto via **Base62**
- [x] Redirecionamento com **HTTP 302** (Temporary Redirect) — escolhido em vez de 301 para permitir contabilizar cliques futuramente
- [x] Validação de URL de entrada com **Pydantic `HttpUrl`** (rejeita `javascript:`, `file://`, URLs sem `http(s)://`)
- [x] Tratamento de erros: **404** (código inexistente) e **422** (payload inválido)
- [x] Documentação automática via **Swagger UI** (`/docs`)
- [x] Testes unitários da lógica de conversão Base62 com `pytest`

## Roadmap

- [ ] Persistência real com **PostgreSQL** (substituir o armazenamento em memória)
- [ ] Camada de cache com **Redis** (otimização para leitura)
- [ ] Testes de integração dos endpoints da API com `TestClient`
- [ ] Proteção contra **SSRF** (bloqueio de IPs privados e metadados de cloud)
- [ ] **Rate limiting** por IP para prevenção de abuso
- [ ] Expiração de links (retorno `410 Gone` para links expirados)
- [ ] Analytics assíncrono de cliques (contagem sem bloquear o redirect)
- [ ] Dockerização (`Dockerfile` + `docker-compose`)
- [ ] Deploy público com documentação final

## Stack Técnica

| Camada | Tecnologia | Motivo da escolha |
|---|---|---|
| Linguagem | **Python 3.14** | Familiaridade do autor e ecossistema maduro |
| Framework Web | **FastAPI** | Alta performance, tipagem nativa, documentação automática |
| Validação | **Pydantic** | Validação declarativa com tipos |
| Gerenciador de pacotes | **uv** | Resolução rápida de dependências e suporte a workspaces |
| Testes | **pytest** | Padrão do ecossistema Python |
| Estrutura | **Monorepo** | Permite compartilhar lógica (`core`) entre serviços (`api`) |

## Estrutura do Repositório
```
URL-Shortener/
├── apps/
│ └── api/ # Servidor FastAPI (endpoints)
│ └── main.py
├── libs/
│ └── core/ # Lógica de negócio compartilhada
│ ├── src/core/base62.py # Algoritmo Base62 (encode/decode)
│ └── tests/test_base62.py
├── pyproject.toml # Configuração do workspace
└── uv.lock # Lockfile de dependências
```
A separação em **monorepo com pacotes independentes** permite que a lógica Base62 (`libs/core`) seja reutilizada por qualquer serviço futuro (CLI, worker, outra API) sem duplicação.

## Decisões de Arquitetura (ADRs resumidos)

**Por que Base62 em vez de hashing (MD5, SHA)?**
Hashing sobre a URL introduz **colisões** (duas URLs gerando o mesmo código). Truncar o hash aumenta ainda mais a chance, e o sistema precisaria consultar o banco a cada geração — inviável em escala. Base62 sobre um **contador incremental único** garante ausência de colisão por construção.

**Por que HTTP 302 e não 301?**
O 301 faz o navegador cachear o redirecionamento, e o servidor **para de receber requisições** — perdendo métricas e inviabilizando expiração/alteração do link. O 302 mantém o servidor no controle do ciclo de vida do link.

**Por que monorepo?**
Permite separar claramente *lógica de negócio* (`core`) de *camada de exposição* (`api`), aplicando o princípio da responsabilidade única e facilitando testes unitários isolados.

## Como rodar localmente

**Pré-requisitos:** Python 3.12+, `uv` instalado.

```bash
# 1. Clonar o repositório
git clone <URL-do-repo>
cd URL-Shortner

# 2. Instalar dependências (o uv resolve o workspace inteiro)
uv sync

# 3. Rodar os testes
uv run pytest

# 4. Subir o servidor de desenvolvimento
cd apps/api
uv run uvicorn main:app --reload

Acesse:
    - API: http://127.0.0.1:8000
    - Swagger UI: http://127.0.0.1:8000/docs