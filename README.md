# Data Sales Platform

Plataforma de Engenharia de Dados desenvolvida para demonstrar, de ponta a ponta, a construção de um pipeline de dados para processamento, qualidade, transformação, modelagem dimensional, armazenamento analítico e visualização de indicadores de vendas.

O projeto utiliza **Python, PostgreSQL, Pandas, Parquet, SQLAlchemy, Alembic, Docker e Streamlit**, aplicando conceitos de **ETL, Data Quality, Data Warehouse, Analytics e BI**.

---

## 🎯 Objetivo

Construir uma plataforma de dados capaz de:

* extrair dados de vendas do PostgreSQL;
* armazenar os dados brutos em formato Parquet;
* executar validações de qualidade;
* transformar os dados para consumo analítico;
* construir dimensões e tabela fato;
* disponibilizar o Data Warehouse em Parquet;
* carregar o Data Warehouse no PostgreSQL;
* executar consultas analíticas;
* disponibilizar indicadores através de um dashboard Streamlit;
* executar testes automatizados;
* permitir a execução completa do processo através de Docker.

O projeto foi estruturado com foco em **boas práticas de Engenharia de Dados, organização de código, testes, observabilidade e reprodutibilidade**.

---

# 🏗️ Arquitetura

```text
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │   Dados de origem   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Ingestion      │
                    │   PostgreSQL →      │
                    │       Parquet       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     data/raw        │
                    │    Dados brutos      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Data Quality     │
                    │ Validação dos dados │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Transformation    │
                    │ Tratamento e        │
                    │ transformação       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   data/processed    │
                    │ Dados processados   │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │         Data Warehouse            │
              │                                  │
              │ dim_cliente                      │
              │ dim_produto                      │
              │ dim_data                         │
              │ fact_vendas                      │
              └───────────────┬──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
          ┌─────────────────┐   ┌─────────────────┐
          │ Parquet         │   │ PostgreSQL      │
          │ Warehouse       │   │ Data Warehouse  │
          └────────┬────────┘   └────────┬────────┘
                   │                     │
                   └──────────┬──────────┘
                              ▼
                    ┌─────────────────────┐
                    │      Analytics      │
                    │ Queries + Services  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    │   dashboard/app.py  │
                    └─────────────────────┘
```

---

# 🔄 Pipeline ETL

O pipeline principal está implementado em:

```text
src/pipeline.py
```

O processo é dividido em **8 etapas**:

### 1. Ingestion

```text
PostgreSQL → data/raw
```

Responsável por extrair os dados da origem e armazená-los em arquivos Parquet.

---

### 2. Data Quality

Validação dos dados brutos antes do processamento.

```text
data/raw
   ↓
Data Quality
```

---

### 3. Transformation

Transformação e preparação dos dados para utilização no Data Warehouse.

```text
data/raw
   ↓
Transformation
   ↓
data/processed
```

---

### 4. Dimensão Cliente

Construção da dimensão:

```text
dim_cliente
```

---

### 5. Dimensão Produto

Construção da dimensão:

```text
dim_produto
```

---

### 6. Dimensão Data

Construção da dimensão:

```text
dim_data
```

---

### 7. Fact Vendas

Construção da tabela fato:

```text
fact_vendas
```

---

### 8. PostgreSQL Data Warehouse

Os arquivos Parquet produzidos pelo Data Warehouse são carregados novamente no PostgreSQL através do módulo:

```text
src/warehouse/postgres_loader.py
```

Dessa forma, o PostgreSQL passa a disponibilizar uma camada analítica estruturada para as consultas do projeto.

---

# 🧰 Tecnologias

| Tecnologia     | Utilização                             |
| -------------- | -------------------------------------- |
| Python 3.11    | Linguagem principal                    |
| PostgreSQL 16  | Banco de dados                         |
| Pandas         | Manipulação e transformação de dados   |
| PyArrow        | Processamento de Parquet               |
| SQLAlchemy     | Acesso ao banco                        |
| Alembic        | Migrações                              |
| Pytest         | Testes automatizados                   |
| Streamlit      | Dashboard                              |
| Docker         | Containerização                        |
| Docker Compose | Orquestração local                     |
| Python-dotenv  | Configuração por variáveis de ambiente |

---

# 📁 Estrutura do projeto

```text
data-sales-platform/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
│
├── logs/
│
├── migrations/
│   ├── versions/
│   └── env.py
│
├── scripts/
│   └── seed_database.py
│
├── src/
│   ├── analytics/
│   │   ├── queries.py
│   │   └── service.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── ingestion/
│   │   └── postgres_to_parquet.py
│   │
│   ├── quality/
│   │   └── parquet_quality.py
│   │
│   ├── transformation/
│   │   └── raw_to_processed.py
│   │
│   ├── warehouse/
│   │   ├── dim_cliente.py
│   │   ├── dim_produto.py
│   │   ├── dim_data.py
│   │   ├── fact_vendas.py
│   │   └── postgres_loader.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   └── metrics.py
│   │
│   └── pipeline.py
│
├── tests/
│
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# ⚙️ Pré-requisitos

Para executar o projeto localmente, é necessário ter instalado:

* Python 3.11 ou superior
* Docker
* Docker Compose
* Git

---

# 🚀 Configuração do ambiente

Clone o projeto:

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre no diretório:

```bash
cd data-sales-platform
```

---

## Ambiente virtual Python

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install .
```

---

# 🔐 Configuração das variáveis de ambiente

Crie um arquivo:

```text
.env
```

Exemplo:

```env
POSTGRES_DB=data_sales
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5433
```

O projeto utiliza o arquivo `.env` para configurar a conexão com o PostgreSQL.

> Não versionar informações reais de acesso ao banco.

---

# 🐳 Execução com Docker

O projeto possui dois serviços:

```text
postgres
pipeline
```

O serviço PostgreSQL utiliza:

```text
postgres:16
```

O pipeline é executado em um container Python 3.11.

Para iniciar o ambiente:

```powershell
docker compose up --build
```

O Docker Compose executará automaticamente:

```text
PostgreSQL
   ↓
Health Check
   ↓
Alembic
   ↓
Seed Database
   ↓
Pipeline ETL
```

O serviço `pipeline` aguarda o PostgreSQL estar saudável antes de iniciar o processamento.

---

# 🔄 Execução automática do Pipeline

O container do pipeline executa:

```text
alembic upgrade head
        ↓
python -m scripts.seed_database
        ↓
python -m src.pipeline
```

Isso significa que, em uma execução completa do ambiente, as migrações são aplicadas, os dados de demonstração são preparados e o pipeline ETL é executado.

---

# ▶️ Executando o Pipeline manualmente

Com o ambiente Python ativado:

```powershell
python -m src.pipeline
```

O pipeline executará as oito etapas:

```text
1/8 - Ingestion
2/8 - Data Quality
3/8 - Transformation
4/8 - Dimensão Cliente
5/8 - Dimensão Produto
6/8 - Dimensão Data
7/8 - Fact Vendas
8/8 - PostgreSQL Data Warehouse
```

---

# 🗄️ Data Warehouse

O Data Warehouse utiliza um modelo dimensional composto por:

```text
dim_cliente
dim_produto
dim_data
fact_vendas
```

### Dimensão Cliente

Contém as informações relacionadas aos clientes.

```text
dim_cliente
```

### Dimensão Produto

Contém as informações relacionadas aos produtos.

```text
dim_produto
```

### Dimensão Data

Fornece a dimensão temporal utilizada pelas análises.

```text
dim_data
```

### Fato Vendas

Centraliza os indicadores relacionados às vendas.

```text
fact_vendas
```

A tabela fato contém informações necessárias para análises de:

* quantidade;
* receita;
* custo;
* lucro;
* margem;
* produto;
* cliente;
* período.

---

# 📊 Data Quality

A qualidade dos dados é executada antes da transformação.

O projeto possui uma etapa específica:

```text
src/quality/parquet_quality.py
```

Essa etapa permite identificar problemas nos dados antes que eles sejam disponibilizados para o Data Warehouse.

Entre as validações utilizadas no projeto estão verificações relacionadas a:

* valores nulos;
* duplicidades;
* consistência dos dados;
* integridade dos registros;
* regras relacionadas aos dados financeiros.

---

# 🔎 Analytics

A camada analítica está localizada em:

```text
src/analytics/
```

Principais componentes:

```text
queries.py
service.py
```

### Queries

Responsável pelas consultas utilizadas para obter os indicadores analíticos.

### Services

Responsável por disponibilizar uma camada de serviço entre as consultas e o dashboard.

Entre os indicadores disponibilizados estão:

* vendas;
* receita;
* lucro;
* margem;
* vendas por produto;
* vendas por cliente;
* evolução mensal;
* análise por período.

---

# 📈 Dashboard

O projeto possui um dashboard desenvolvido com Streamlit.

Arquivo principal:

```text
dashboard/app.py
```

Para executar:

```powershell
streamlit run dashboard/app.py
```

O dashboard permite selecionar o período de análise e visualizar indicadores de vendas.

### Indicadores

São apresentados indicadores como:

```text
Quantidade
Receita
Lucro
Margem
```

### Análises

O dashboard apresenta:

* evolução mensal das vendas;
* vendas por produto;
* detalhes dos produtos;
* margem por produto;
* vendas por cliente;
* detalhes dos clientes.

---

# 🧪 Testes

Os testes automatizados são executados utilizando Pytest.

Para executar:

```powershell
pytest
```

O projeto possui testes unitários e testes de integração.

Para executar especificamente os testes de integração:

```powershell
pytest -m integration
```

Os testes têm como objetivo validar componentes individuais e também o funcionamento integrado do pipeline.

---

# 📐 Resultados atuais

Na versão atual do projeto, o Data Warehouse apresenta:

| Tabela      | Registros |
| ----------- | --------: |
| dim_cliente |        10 |
| dim_produto |        20 |
| dim_data    |        15 |
| fact_vendas |     2.909 |

Indicadores financeiros atualmente validados:

| Indicador            |       Resultado |
| -------------------- | --------------: |
| Receita total        | R$ 7.475.020,30 |
| Custo total          | R$ 5.547.000,00 |
| Lucro total          | R$ 1.928.020,30 |
| Margem média         |          31,31% |
| Receita igual a zero |               0 |
| IDs duplicados       |               0 |
| Nulos críticos       |               0 |

Esses números representam a execução atual do pipeline e podem mudar caso a massa de dados seja alterada.

---

# 🗃️ Banco de dados e Alembic

O projeto utiliza **Alembic** para controle de evolução do banco de dados.

As migrações ficam em:

```text
migrations/versions/
```

Para aplicar as migrações:

```powershell
alembic upgrade head
```

Para verificar a versão atual:

```powershell
alembic current
```

Para visualizar o histórico:

```powershell
alembic history
```

---

# 📝 Logs

O pipeline possui mecanismo de logging através de:

```text
src/utils/logger.py
```

As métricas de execução são controladas por:

```text
src/utils/metrics.py
```

Cada etapa do pipeline possui medição de tempo, permitindo acompanhar a execução do processo.

Os logs são armazenados no diretório:

```text
logs/
```

---

# 🔁 Como reproduzir o projeto do zero

Uma nova máquina pode executar o projeto seguindo o fluxo abaixo.

### 1. Clonar o projeto

```powershell
git clone <URL_DO_REPOSITORIO>
cd data-sales-platform
```

### 2. Criar o `.env`

```env
POSTGRES_DB=data_sales
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5433
```

### 3. Subir o ambiente

```powershell
docker compose up --build
```

### 4. Verificar o pipeline

Os logs podem ser acompanhados através do Docker:

```powershell
docker compose logs -f pipeline
```

### 5. Executar o dashboard

Com o ambiente Python configurado:

```powershell
streamlit run dashboard/app.py
```

### 6. Executar os testes

```powershell
pytest
```

---

# 🧠 Decisões arquiteturais

## Por que Parquet?

O projeto utiliza Parquet como formato intermediário e de armazenamento porque ele é adequado para workloads analíticos e processamento de dados tabulares.

O uso de Parquet também permite separar as diferentes etapas do pipeline:

```text
raw
processed
warehouse
```

---

## Por que PostgreSQL?

O PostgreSQL é utilizado tanto como fonte dos dados quanto como camada final do Data Warehouse.

Essa abordagem permite demonstrar:

```text
OLTP / Fonte
     ↓
Processamento
     ↓
Data Warehouse
     ↓
Analytics
```

---

## Por que Docker?

Docker permite reproduzir o ambiente de execução de forma consistente, reduzindo dependências relacionadas à configuração da máquina.

---

## Por que Streamlit?

Streamlit permite disponibilizar rapidamente uma camada de visualização sobre os dados produzidos pelo pipeline.

Dessa forma, o projeto demonstra não apenas a construção do pipeline, mas também o consumo dos dados por uma aplicação analítica.

---

# 🔮 Próximas evoluções

Possíveis evoluções do projeto:

* implementação de orquestração com Airflow;
* inclusão de processamento distribuído com Spark;
* criação de testes de Data Quality mais abrangentes;
* implementação de CI/CD;
* monitoramento do pipeline;
* criação de métricas de observabilidade;
* execução incremental do pipeline;
* particionamento dos dados;
* implementação de estratégia de carga incremental no Data Warehouse;
* disponibilização da camada analítica através de API;
* implantação em ambiente cloud;
* criação de infraestrutura como código.

---

# 💼 Objetivo profissional

Este projeto faz parte do meu portfólio de transição e especialização em **Engenharia de Dados**, demonstrando experiência prática com:

```text
Python
SQL
PostgreSQL
ETL
Data Quality
Parquet
Data Warehouse
Modelagem Dimensional
Analytics
Docker
Testes Automatizados
Streamlit
```

A proposta é demonstrar a capacidade de construir uma solução de dados **de ponta a ponta**, desde a ingestão até a disponibilização dos indicadores para o usuário final.

---

# 👨‍💻 Autor

**Anderson Soares**

Analista de Sistemas Sênior | Integração de Dados | Oracle | Engenharia de Dados | Backend Python

---

## 📌 Licença

Projeto desenvolvido para fins de estudo, demonstração técnica e portfólio profissional.
