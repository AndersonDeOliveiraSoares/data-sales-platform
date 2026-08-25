# Data Sales Platform

Pipeline de Engenharia de Dados desenvolvido em Python para demonstrar, de ponta a ponta, um fluxo de ingestão, qualidade, transformação e construção de um Data Warehouse analítico.

O projeto utiliza PostgreSQL como fonte de dados, Parquet como formato de armazenamento intermediário e um modelo dimensional com dimensões e tabela fato para análise de vendas.

---

## 1. Visão geral

O projeto implementa um pipeline de dados com as seguintes etapas:

```text
PostgreSQL
    │
    ▼
Ingestion
    │
    ▼
data/raw
    │
    ▼
Data Quality
    │
    ▼
Transformation
    │
    ▼
data/processed
    │
    ▼
Data Warehouse
    ├── dim_cliente
    ├── dim_produto
    ├── dim_data
    └── fact_vendas
```

O pipeline pode ser executado diretamente no ambiente Python ou completamente utilizando Docker.

---

## 2. Objetivo

O objetivo do projeto é construir um pipeline de dados completo, reproduzível e testável, aplicando conceitos fundamentais de Engenharia de Dados:

* Ingestão de dados;
* Processamento e transformação;
* Data Quality;
* Armazenamento em Parquet;
* Modelagem dimensional;
* Construção de tabelas fato e dimensões;
* Observabilidade através de logs;
* Métricas de execução;
* Testes automatizados;
* Containerização com Docker;
* Migrações de banco de dados;
* Preparação para futura orquestração.

O projeto também funciona como portfólio técnico para demonstrar conhecimentos práticos de Engenharia de Dados e Backend Python.

---

## 3. Arquitetura

### Arquitetura atual

```text
                         ┌─────────────────────┐
                         │     PostgreSQL 16   │
                         │                     │
                         │ cliente             │
                         │ produto             │
                         │ pedido              │
                         │ item_pedido         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Ingestion       │
                         │ PostgreSQL → Pandas │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      data/raw       │
                         │      Parquet        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Data Quality     │
                         │                     │
                         │ Schema              │
                         │ Not Null            │
                         │ Unique              │
                         │ Non Negative       │
                         │ Positive            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Transformation    │
                         │    Raw → Processed  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   data/processed    │
                         │       Parquet       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │        Data Warehouse         │
                    │                               │
                    │  dim_cliente                  │
                    │  dim_produto                  │
                    │  dim_data                    │
                    │  fact_vendas                  │
                    └───────────────────────────────┘
```

---

## 4. Fluxo do pipeline

O pipeline principal está implementado em:

```text
src/pipeline.py
```

A execução possui sete etapas:

### 1. Ingestion

Extrai os dados do PostgreSQL e grava os dados em arquivos Parquet:

```text
PostgreSQL
    ↓
data/raw/
```

Tabelas:

* `cliente`
* `produto`
* `pedido`
* `item_pedido`

---

### 2. Data Quality

Valida os dados antes do processamento.

São realizadas verificações de:

* existência das colunas obrigatórias;
* valores nulos;
* valores negativos;
* valores que devem ser positivos;
* duplicidade de identificadores;
* chaves únicas.

Caso uma validação falhe, o pipeline interrompe a execução.

---

### 3. Transformation

Transforma os dados da camada `raw` para a camada `processed`.

```text
data/raw
    ↓
Transformation
    ↓
data/processed
```

Cada entidade possui sua própria transformação.

---

### 4. Dimensão Cliente

Cria:

```text
data/warehouse/dim_cliente.parquet
```

A dimensão contém:

* `id_cliente`
* `nome`
* `cidade`
* `estado`

Resultado atual:

```text
10 registros
```

---

### 5. Dimensão Produto

Cria:

```text
data/warehouse/dim_produto.parquet
```

A dimensão contém informações como:

* produto;
* categoria;
* subcategoria;
* preço de venda;
* preço de custo.

Resultado atual:

```text
20 registros
```

---

### 6. Dimensão Data

Cria:

```text
data/warehouse/dim_data.parquet
```

A dimensão possui atributos derivados da data:

* data;
* ano;
* mês;
* nome do mês;
* trimestre;
* dia;
* dia da semana;
* nome do dia da semana.

Resultado atual:

```text
15 registros
```

---

### 7. Fact Vendas

A tabela fato é construída a partir dos pedidos e itens de pedidos, enriquecidos pelas dimensões.

Arquivo:

```text
data/warehouse/fact_vendas.parquet
```

A tabela contém informações como:

* pedido;
* cliente;
* produto;
* data;
* quantidade;
* preço unitário;
* subtotal;
* custo total;
* receita;
* lucro;
* margem;
* frete;
* status do pedido;
* forma de pagamento.

Resultado atual:

```text
30 registros
```

---

## 5. Modelo dimensional

O Data Warehouse utiliza uma abordagem baseada em modelo dimensional.

```text
                    dim_cliente
                         │
                         │
                         ▼
dim_data ────────── fact_vendas ────────── dim_produto
```

### Dimensões

```text
dim_cliente
dim_produto
dim_data
```

### Fato

```text
fact_vendas
```

A `fact_vendas` contém as métricas utilizadas para análise comercial.

Exemplos:

```text
receita
custo_total
lucro
margem
quantidade
```

---

## 6. Cálculos analíticos

A tabela fato calcula indicadores básicos de vendas.

### Custo total

```text
custo_total =
    preco_custo × quantidade
```

### Receita

```text
receita =
    subtotal
```

### Lucro

```text
lucro =
    receita - custo_total
```

### Margem

```text
margem =
    lucro / receita
```

Essas métricas permitem utilizar o Data Warehouse posteriormente para análises como:

* receita por produto;
* lucro por produto;
* margem por categoria;
* vendas por cliente;
* vendas por período;
* produtos mais vendidos.

---

## 7. Data Quality

A camada de qualidade está implementada em:

```text
src/quality/parquet_quality.py
```

As validações atuais incluem:

### Schema

Verificação das colunas obrigatórias.

### Not Null

Verificação de valores nulos em campos obrigatórios.

### Valores não negativos

Aplicada a campos como:

```text
preco_venda
preco_custo
quantidade_estoque
valor_total
valor_frete
preco_unitario
subtotal
```

### Valores positivos

Aplicada principalmente à quantidade dos itens:

```text
quantidade > 0
```

### Unicidade

Verificação de duplicidade em identificadores e campos únicos.

---

## 8. Observabilidade

O projeto possui logging centralizado através de:

```text
src/utils/logger.py
```

Os logs são enviados para:

```text
console
logs/pipeline.log
```

Exemplo:

```text
2026-08-25 17:59:51 | INFO | ingestion |
cliente: 10 registros -> data/raw/cliente.parquet
```

O pipeline também registra métricas de execução através de:

```text
src/utils/metrics.py
```

São registrados:

* início da etapa;
* término da etapa;
* duração da etapa;
* quantidade de registros;
* duração total do pipeline.

Exemplo:

```text
Etapa concluída | step=7/7 - Fact Vendas | duration=0.14s
Pipeline finalizado | duration=0.60s
```

---

## 9. Métricas atuais

Uma execução completa apresentou:

| Etapa            | Registros |
| ---------------- | --------: |
| Clientes         |        10 |
| Produtos         |        20 |
| Pedidos          |        15 |
| Itens de pedido  |        30 |
| Ingestion        |        75 |
| Data Quality     |        75 |
| Dimensão Cliente |        10 |
| Dimensão Produto |        20 |
| Dimensão Data    |        15 |
| Fact Vendas      |        30 |

Tempo total observado em execução Docker:

```text
0.60s
```

---

## 10. Testes automatizados

O projeto possui testes automatizados utilizando `pytest`.

Execução:

```bash
python -m pytest -q
```

Resultado atual:

```text
171 passed
```

Os testes cobrem diferentes componentes do projeto, incluindo:

* banco de dados;
* modelos;
* API;
* transformações;
* Data Quality;
* pipeline;
* warehouse;
* integração.

A execução dos testes também é utilizada no CI.

---

## 11. Banco de dados

O banco utilizado é:

```text
PostgreSQL 16
```

As principais tabelas são:

```text
cliente
produto
pedido
item_pedido
```

O acesso é realizado através de:

```text
SQLAlchemy
```

As alterações estruturais do banco são controladas através de:

```text
Alembic
```

---

## 12. Seed de dados

Para facilitar testes e demonstrações, o projeto possui um script de carga inicial:

```text
scripts/seed_database.py
```

Execução:

```bash
python -m scripts.seed_database
```

O seed cria:

```text
10 clientes
20 produtos
15 pedidos
30 itens de pedido
```

Os dados são propositalmente pequenos para permitir execução rápida e previsível do pipeline.

---

## 13. Docker

O projeto possui Docker Compose para executar o PostgreSQL e o pipeline.

Serviços atuais:

```text
postgres
pipeline
```

O PostgreSQL é executado em:

```text
localhost:5433
```

Dentro da rede Docker, o pipeline acessa o banco através de:

```text
postgres:5432
```

### Build da imagem

```bash
docker compose build pipeline
```

### Execução do pipeline

```bash
docker compose up pipeline
```

O fluxo executado pelo container é:

```text
Alembic
    ↓
Seed
    ↓
Pipeline
```

O pipeline é executado completamente dentro do container.

Os diretórios de dados e logs são montados como volumes:

```text
data/
logs/
```

Isso permite visualizar os arquivos gerados pelo pipeline no ambiente local.

---

## 14. Estrutura do projeto

```text
data-sales-platform/
│
├── .github/
│   └── workflows/
│       └── ...
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
│
├── database/
│
├── logs/
│
├── migrations/
│
├── scripts/
│   └── seed_database.py
│
├── src/
│   │
│   ├── api/
│   │
│   ├── database/
│   │
│   ├── ingestion/
│   │   └── postgres_to_parquet.py
│   │
│   ├── quality/
│   │   └── parquet_quality.py
│   │
│   ├── transformation/
│   │   ├── cliente_transformation.py
│   │   ├── produto_transformation.py
│   │   ├── pedido_transformation.py
│   │   ├── item_pedido_transformation.py
│   │   └── raw_to_processed.py
│   │
│   ├── warehouse/
│   │   ├── dim_cliente.py
│   │   ├── dim_produto.py
│   │   ├── dim_data.py
│   │   └── fact_vendas.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   └── metrics.py
│   │
│   └── pipeline.py
│
├── tests/
│
├── .env.example
├── .env.test
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 15. Tecnologias

### Linguagem

```text
Python 3.11
```

### Processamento

```text
Pandas
PyArrow
```

### Banco de dados

```text
PostgreSQL 16
SQLAlchemy
Alembic
```

### API

```text
FastAPI
Uvicorn
```

### Testes

```text
Pytest
HTTPX
```

### Infraestrutura

```text
Docker
Docker Compose
```

### Armazenamento

```text
Parquet
```

---

## 16. Configuração do ambiente

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar no Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Instalar o projeto

```bash
pip install -e .
```

### Configurar variáveis de ambiente

Copie:

```text
.env.example
```

para:

```text
.env
```

Configure as credenciais do PostgreSQL.

---

## 17. Execução local

Com o PostgreSQL disponível:

### Aplicar migrations

```bash
alembic upgrade head
```

### Carregar dados

```bash
python -m scripts.seed_database
```

### Executar o pipeline

```bash
python -m src.pipeline
```

O pipeline produzirá:

```text
data/raw/
data/processed/
data/warehouse/
logs/
```

---

## 18. Execução com Docker

Subir o PostgreSQL:

```bash
docker compose up -d postgres
```

Construir a imagem:

```bash
docker compose build pipeline
```

Executar o pipeline:

```bash
docker compose up pipeline
```

---

## 19. Validação do resultado

Após a execução, os arquivos esperados no warehouse são:

```text
data/warehouse/
├── dim_cliente.parquet
├── dim_produto.parquet
├── dim_data.parquet
└── fact_vendas.parquet
```

Quantidade atual esperada:

```text
dim_cliente.parquet → 10
dim_produto.parquet → 20
dim_data.parquet    → 15
fact_vendas.parquet → 30
```

---

## 20. CI/CD

O projeto possui pipeline de integração contínua para executar os testes automatizados.

O objetivo é garantir que alterações no código não introduzam regressões.

A validação atual do projeto apresenta:

```text
171 testes aprovados
```

---

## 21. Decisões técnicas

### PostgreSQL

Escolhido como banco relacional de origem por ser amplamente utilizado em ambientes corporativos e adequado para demonstrar integração com sistemas transacionais.

### Parquet

Utilizado como formato de armazenamento por ser eficiente para processamento analítico e integração com ferramentas de dados.

### Pandas

Utilizado para as transformações por oferecer uma API simples para manipulação tabular e integração direta com Parquet.

### Modelo dimensional

A utilização de dimensões e fato demonstra conceitos fundamentais de Data Warehouse e facilita análises posteriores.

### Docker

Utilizado para garantir maior reprodutibilidade do ambiente e reduzir diferenças entre ambientes de execução.

### Pytest

Utilizado para garantir qualidade e permitir evolução segura do projeto.

---

## 22. Características de Engenharia de Dados demonstradas

Este projeto demonstra conhecimentos em:

* ETL;
* ELT;
* ingestão de dados;
* processamento batch;
* armazenamento em Parquet;
* Data Quality;
* modelagem dimensional;
* Data Warehouse;
* tabelas fato;
* dimensões;
* métricas;
* logging;
* testes automatizados;
* integração contínua;
* Docker;
* PostgreSQL;
* SQLAlchemy;
* Alembic;
* Python;
* arquitetura modular.

---

## 23. Próximos passos

O projeto continuará evoluindo para uma arquitetura mais próxima de um ambiente profissional.

### Próximas evoluções planejadas

* [ ] Documentar arquitetura detalhadamente;
* [ ] Separar seed de dados da execução normal do pipeline;
* [ ] Melhorar tratamento de erros;
* [ ] Implementar estratégias de retry;
* [ ] Adicionar mais regras de Data Quality;
* [ ] Evoluir métricas e observabilidade;
* [ ] Adicionar análises sobre o Data Warehouse;
* [ ] Implementar orquestração com Apache Airflow;
* [ ] Criar DAG do pipeline;
* [ ] Implementar agendamento;
* [ ] Implementar dependências entre tarefas;
* [ ] Implementar retry e controle de falhas no Airflow.

---

## 24. Objetivo profissional

Este projeto faz parte de uma jornada prática de evolução para Engenharia de Dados.

A proposta é demonstrar não apenas conhecimento isolado de ferramentas, mas a capacidade de construir um pipeline completo envolvendo:

```text
Fonte de dados
      ↓
Ingestão
      ↓
Qualidade
      ↓
Transformação
      ↓
Armazenamento
      ↓
Modelagem dimensional
      ↓
Data Warehouse
      ↓
Observabilidade
      ↓
Testes
      ↓
Containerização
      ↓
Orquestração
```

A próxima grande evolução da arquitetura será a introdução de **Apache Airflow** para orquestração do pipeline.

---

## Status atual

```text
Pipeline ETL              ✅
PostgreSQL                ✅
Alembic                   ✅
Data Quality              ✅
Parquet                   ✅
Transformation            ✅
Data Warehouse            ✅
Fact/Dimensions           ✅
Logging                   ✅
Pipeline Metrics          ✅
Automated Tests           ✅
CI                        ✅
Docker                    ✅
Architecture              🚧
Airflow                   ⏳
```

**Projeto em evolução contínua.**
