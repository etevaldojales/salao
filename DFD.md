# Diagrama de Fluxo de Dados (DFD) - Sistema de Gerenciamento de Salão

## Visão Geral do Sistema

Este documento apresenta o Diagrama de Fluxo de Dados (DFD) para o sistema de gerenciamento de salão de beleza, desenvolvido em Django com banco de dados MySQL.

---

## Nível 0 - Contexto do Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SISTEMA DE GERENCIAMENTO                       │
│                              DE SALÃO                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌─────────────┬─────────────┼─────────────┬─────────────┐
        │             │             │             │             │
        ▼             ▼             ▼             ▼             ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Cliente  │  │Profiss. │  │Admin    │  │Sistema  │  │Relatórios│
   │         │  │         │  │         │  │Autent.  │  │         │
   └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

---

## Nível 1 - Decomposição do Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SISTEMA DE SALÃO                                      │
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  Autenticação│    │Gerenciamento │    │  Agendamento │    │Relatórios │ │
│  │   de Usuário │    │   de Dados   │    │   de Serviços │   │  e Estat. │ │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └─────┬─────┘ │
│         │                   │                   │                   │       │
│         └───────────────────┼───────────────────┼───────────────────┘       │
│                             │                   │                           │
│                        ┌────▼───────────────────▼────┐                       │
│                        │      BANCO DE DADOS          │                       │
│                        │   (MySQL - salao_banco)      │                       │
│                        └──────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Nível 2 - Detalhamento dos Processos

### 2.1 Autenticação de Usuário

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSO: AUTENTICAÇÃO                         │
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    │
│   │   Login     │───▶│  Validar    │───▶│  Criar Sessão   │    │
│   │  (form)     │    │  Credenciais│    │  (session)      │    │
│   └─────────────┘    └─────────────┘    └─────────────────┘    │
│         │                                    │                  │
│         │         ┌─────────────┐            │                  │
│         └────────▶│  Registro   │────────────┘                  │
│                   │  (novo user)│                                 │
│                   └─────────────┘                                 │
│                                                                 │
│   Entidades Externas:                                           │
│   - Cliente (pode se registrar)                                 │
│   - Administrador (acesso total)                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Gerenciamento de Dados (CRUD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PROCESSO: GERENCIAMENTO DE DADOS                         │
│                                                                             │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │    Cliente   │    │   Serviço    │    │  Profissional│                 │
│   │   (CRUD)     │    │   (CRUD)     │    │   (CRUD)     │                 │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                 │
│          │                    │                    │                        │
│          ▼                    ▼                    ▼                        │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                   DATA STORE: CLIENTES                   │              │
│   │   - id (PK)                                              │              │
│   │   - nome                                                 │              │
│   │   - email                                                │              │
│   │   - telefone                                             │              │
│   │   - deleted_at (soft delete)                            │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                   DATA STORE: SERVIÇOS                   │              │
│   │   - id (PK)                                              │              │
│   │   - nome                                                 │              │
│   │   - preco                                                │              │
│   │   - deleted_at (soft delete)                            │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                DATA STORE: PROFISSIONAIS                 │              │
│   │   - id (PK)                                              │              │
│   │   - nome                                                 │              │
│   │   - especialidade                                        │              │
│   │   - deleted_at (soft delete)                            │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                DATA STORE: USUÁRIOS (Django Auth)       │              │
│   │   - id (PK)                                              │              │
│   │   - username                                             │              │
│   │   - password (hashed)                                   │              │
│   │   - is_staff                                             │              │
│   └─────────────────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Agendamento de Serviços

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 PROCESSO: AGENDAMENTO DE SERVIÇOS                          │
│                                                                             │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                      FLUXO DE AGENDAMENTO                          │    │
│   │                                                                     │    │
│   │   ┌─────────┐    ┌─────────────┐    ┌──────────────┐             │    │
│   │   │ Cliente │───▶│ Selecionar  │───▶│ Escolher     │             │    │
│   │   │         │    │ Serviço     │    │ Profissional │             │    │
│   │   └─────────┘    └─────────────┘    └──────┬───────┘             │    │
│   │                                              │                      │    │
│   │                                              ▼                      │    │
│   │                                    ┌──────────────┐                │    │
│   │                                    │ Definir Data │                │    │
│   │                                    │    e Hora    │                │    │
│   │                                    └──────┬───────┘                │    │
│   │                                           │                        │    │
│   │                                           ▼                        │    │
│   │                                    ┌──────────────┐                │    │
│   │                                    │ Validar      │                │    │
│   │                                    │ Disponibil.  │                │    │
│   │                                    └──────┬───────┘                │    │
│   │                                           │                        │    │
│   │                                           ▼                        │    │
│   │                                    ┌──────────────┐                │    │
│   │                                    │   SALVAR     │                │    │
│   │                                    │ Agendamento  │                │    │
│   │                                    └──────────────┘                │    │
│   └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                    DATA STORE: AGENDAMENTOS                         │    │
│   │   - id (PK)                                                         │    │
│   │   - cliente_id (FK) ─────────▶ Clientes                            │    │
│   │   - servico_id (FK) ──────────▶ Serviços                           │    │
│   │   - profissional_id (FK) ─────▶ Profissionais                     │    │
│   │   - data_hora (DateTime)                                            │    │
│   │   - status (AGENDADO/CONCLUIDO/CANCELADO)                          │    │
│   │   - deleted_at (soft delete)                                       │    │
│   │                                                                     │    │
│   │   Índice: (status, data_hora)                                      │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   STATUS DO AGENDAMENTO:                                                   │
│   ┌────────────┐    ┌────────────┐    ┌────────────┐                      │
│   │  AGENDADO  │───▶│ CONCLUIDO  │    │ CANCELADO  │                      │
│   └────────────┘    └────────────┘    └────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Relatórios e Estatísticas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PROCESSO: RELATÓRIOS                                   │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                         TIPOS DE RELATÓRIO                            │ │
│   │                                                                       │ │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │ │
│   │  │ Agendamentos   │  │  Faturamento   │  │  Serviços mais│         │ │
│   │  │ por Dia/Mês    │  │  (receita)     │  │  solicitados  │         │ │
│   │  └────────────────┘  └────────────────┘  └────────────────┘         │ │
│   │                                                                       │ │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │ │
│   │  │ Performance de │  │  Status dos   │  │ Top 10        │         │ │
│   │  │ Profissionais   │  │  Agendamentos │  │ Clientes      │         │ │
│   │  └────────────────┘  └────────────────┘  └────────────────┘         │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│   PARÂMETROS DE FILTRO:                                                    │
│   - data_inicio (YYYY-MM-DD)                                               │
│   - data_fim (YYYY-MM-DD)                                                  │
│   - periodo (dia/mes) - para relatórios temporais                          │
│                                                                             │
│   FLUXO DE DADOS:                                                           │
│                                                                             │
│   Request GET ──▶ Processar Filtros ──▶ Query Database ──▶ JSON Response  │
│                                                                             │
│   Endpoints:                                                                │
│   - /relatorios/dados/          → dados_relatorio                         │
│   - /relatorios/faturamento/    → dados_relatorio_faturamento              │
│   - /relatorios/servicos/       → dados_relatorio_servicos                  │
│   - /relatorios/profissionais/  → dados_relatorio_profissionais            │
│   - /relatorios/status/         → dados_relatorio_status                   │
│   - /relatorios/clientes/       → dados_relatorio_clientes                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Entidades Externas (Atores)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    CLIENTE      │     │  PROFISSIONAL   │     │  ADMINISTRADOR │
│                 │     │                 │     │                 │
│ - Agenda        │     │ - Executa       │     │ - Gerencia     │
│   serviços      │     │   serviços      │     │   usuários     │
│ - Visualiza     │     │ - Atualiza      │     │ - CRUD completo│
│   histórico     │     │   agenda        │     │ - Visualiza    │
│                 │     │                 │     │   relatórios   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Fluxo de Dados Principal

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUXO PRINCIPAL DE DADOS                                │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────────┐    ┌───────────────────┐   │
│  │ Cliente │───▶│ Form    │───▶│  Validation │───▶│   Banco de Dados  │   │
│  │Request │    │ (POST)  │    │  (Django)   │    │   (MySQL)         │   │
│  └─────────┘    └─────────┘    └─────────────┘    └───────────────────┘   │
│       │                                                      │              │
│       │         ┌──────────────────────────────────────────┘              │
│       │         │                                                           │
│       ▼         ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    RESPONSE (HTML/JSON)                             │    │
│  │  - Render templates (HTML)                                          │    │
│  │  - JsonResponse (para relatórios)                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tabelas do Banco de Dados

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ESTRUTURA DO BANCO DE DADOS                         │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │     Cliente      │  │     Servico       │  │    Profissional  │        │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤        │
│  │ id (PK)          │  │ id (PK)          │  │ id (PK)          │        │
│  │ nome             │  │ nome             │  │ nome             │        │
│  │ email            │  │ preco            │  │ especialidade    │        │
│  │ telefone         │  │ deleted_at       │  │ deleted_at       │        │
│  │ deleted_at       │  └──────────────────┘  └──────────────────┘        │
│  └──────────────────┘                                                      │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │    Agendamento   │  │       User       │  │     Agendamento  │        │
│  │   (principal)    │  │   (Django Auth)  │  │      Index       │        │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤        │
│  │ id (PK)          │  │ id (PK)          │  │ status           │        │
│  │ cliente_id (FK)  │  │ username         │  │ data_hora        │        │
│  │ servico_id (FK)  │  │ password         │  │ (índice composto)│        │
│  │ profissional_id  │  │ is_staff         │  └──────────────────┘        │
│  │ data_hora        │  └──────────────────┘                               │
│  │ status           │                                                    │
│  │ deleted_at       │                                                    │
│  └──────────────────┘                                                    │
│                                                                             │
│  RELACIONAMENTOS:                                                          │
│  Agendamento 1:N Cliente                                                   │
│  Agendamento 1:N Servico                                                   │
│  Agendamento 1:N Profissional                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tecnologias Utilizadas

| Componente       | Tecnologia          |
|------------------|--------------------|
| Backend          | Django 6.0         |
| Banco de Dados   | MySQL              |
| Autenticação     | Django Auth        |
| Frontend         | HTML/CSS/JS        |
| Soft Delete      | django-softdelete  |
| Deploy           | Docker             |

---

## Referência de Endpoints

| Rota                        | Função                    | Método |
|-----------------------------|---------------------------|--------|
| /                           | Lista agendamentos        | GET    |
| /novo/                      | Criar agendamento         | GET/POST |
| /editar/<id>/               | Editar agendamento        | GET/POST |
| /clientes/                  | Lista clientes            | GET    |
| /clientes/novo/             | Criar cliente             | GET/POST |
| /servicos/                  | Lista serviços            | GET    |
| /servicos/novo/            | Criar serviço             | GET/POST |
| /profissionais/             | Lista profissionais       | GET    |
| /profissionais/novo/       | Criar profissional        | GET/POST |
| /relatorios/                | Painel de relatórios      | GET    |
| /relatorios/dados/          | Dados básica              | GET    |
| /relatorios/faturamento/   | Faturamento               | GET    |
| /usuarios/                  | Gerenciar usuários        | GET    |
| /register/                  | Registro de usuário       | GET/POST |
| /login/                     | Login                     | GET/POST |

---

*Documento gerado automaticamente para o Sistema de Gerenciamento de Salão*
*Versão 1.0*
