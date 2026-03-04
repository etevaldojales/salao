# Diagrama de Fluxo de Dados (DFD) - Sistema de Agendamentos de Salão

## Visão Geral

Este documento apresenta o Diagrama de Fluxo de Dados (DFD) para o Sistema de Gerenciamento de Agendamentos de Salão. O DFD描绘a como os dados fluem através do sistema, incluindo processos, armazenamentos de dados, entidades externas e fluxos de dados.

---

## Diagrama de Contexto (Nível 0)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SISTEMA DE AGENDAMENTOS                             │
│                                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Cliente  │    │Profissional│   │ Servico  │    │ Admin    │            │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘            │
│       │               │               │               │                   │
│       │    ┌──────────▼──────────────▼──────────────┐                   │
│       └────►                                    ◄────┘                   │
│            │     SISTEMA DE AGENDAMENTOS           │                     │
│            │                                        │                     │
│            │   ┌────────────────────────────────┐  │                     │
│            └──►│  Gerenciamento de Agendamentos │──┘                     │
│                 └────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama de Nível 1

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA DE AGENDAMENTOS DE SALÃO                          │
│                                                                                      │
│                                                                                      │
│  ┌──────────────┐                                                                         │
│  │   CLIENTE    │                                                                         │
│  └──────┬───────┘                                                                         │
│         │                                                                               │
│         │ 1. Dados do Cliente                                                            │
│         ▼                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────────┐           │
│  │  P1: GERENCIAMENTO DE CLIENTES                                           │           │
│  │  ─────────────────────────────────────                                   │           │
│  │  • Cadastrar cliente                                                    │           │
│  │  • Atualizar cliente                                                    │           │
│  │  • Excluir cliente                                                     │           │
│  │  • Listar clientes                                                      │           │
│  └───────┬──────────────────────────────────────────────┬────────────────────┘           │
│          │ 2. Dados do Cliente                         │                              │
│          │                                             │                              │
│          ▼                                             ▼                              │
│  ┌────────────────────────────────┐    ┌────────────────────────────────────────┐      │
│  │     ARMAZENAMENTO:             │    │  P2: GERENCIAMENTO DE AGENDAMENTOS    │      │
│  │     CLIENTES                   │    │  ─────────────────────────────────    │      │
│  │     ─────────────              │    │  • Criar agendamento                  │      │
│  │     • id                       │    │  • Editar agendamento                 │      │
│  │     • nome                     │    │  • Cancelar agendamento               │      │
│  │     • email                    │    │  • Listar agendamentos                │      │
│  │     • telefone                 │    │  • Atualizar status                   │      │
│  └────────────────────────┬───────┘    └─────────────────────┬────────────────────┘      │
│                           │                                   │                            │
│                           │ 3. Dados de Agendamento          │                            │
│                           │ 4. Solicitação de Agendamento    │                            │
│                           ▼                                   │                            │
│  ┌──────────────┐                                   ┌────────▼─────────┐               │
│  │  SERVIÇO     │                                   │  AGENDAMENTOS   │               │
│  └──────┬───────┘                                   └────────┬────────┘               │
│         │                                                    │                          │
│         │ 5. Dados do Serviço                                │                          │
│         ▼                                                    │                          │
│  ┌──────────────────────────────────────────────┐           │                          │
│  │  P3: GERENCIAMENTO DE SERVIÇOS                │           │                          │
│  │  ─────────────────────────────────           │           │                          │
│  │  • Cadastrar serviço                          │           │                          │
│  │  • Atualizar serviço                         │           │                          │
│  │  • Excluir serviço                           │           │                          │
│  │  • Listar serviços                           │           │                          │
│  └───────────────┬──────────────────────────────┘           │                          │
│                  │ 6. Dados do Serviço                       │                          │
│                  │                                            │                          │
│                  ▼                                            │                          │
│  ┌────────────────────────────────┐                          │                          │
│  │     ARMAZENAMENTO:             │    ┌─────────────────────▼──────────────┐             │
│  │     SERVIÇOS                   │    │  P4: GERENCIAMENTO DE              │             │
│  │     ─────────                  │    │  PROFISSIONAIS                    │             │
│  │     • id                       │    │  ───────────────────              │             │
│  │     • nome                     │    │  • Cadastrar profissional         │             │
│  │     • preco                    │    │  • Atualizar profissional         │             │
│  │     • duracao                  │    │  • Excluir profissional            │             │
│  └─────────────┬──────────────────┘    │  • Listar profissionais           │             │
│                │ 7. Dados do            │  ─────────────────────────────     │             │
│                │    Profissional        └──────────────┬───────────────────┘             │
│                ▼                                        │                                 │
│  ┌────────────────────────────┐                         │                                 │
│  │     ARMAZENAMENTO:         │                         │                                 │
│  │     PROFISSIONAIS          │                         │                                 │
│  │     ─────────────          │                         │                                 │
│  │     • id                   │                         │                                 │
│  │     • nome                 │                         │                                 │
│  │     • especialidade        │                         │                                 │
│  └────────────────────────────┘                         │                                 │
│                                                         │                                 │
│  ┌──────────────┐                                        │                                 │
│  │ ADMINISTRADOR│                                        │                                 │
│  └──────┬───────┘                                        │                                 │
│         │ 8. Solicitações de Relatório                   │                                 │
│         │ 9. Comandos de Gerenciamento                   │                                 │
│         ▼                                                │                                 │
│  ┌──────────────────────────────────────────────────────┴──────────────────────────┐    │
│  │  P5: GERENCIAMENTO DE RELATÓRIOS                                            │         │
│  │  ────────────────────────────                                               │         │
│  │  • Gerar relatório de agendamentos                                          │         │
│  │  • Gerar relatório de faturamento                                           │         │
│  │  • Gerar relatório de serviços                                             │         │
│  │  • Gerar relatório de profissionais                                         │         │
│  │  • Gerar relatório de clientes                                             │         │
│  │  • Gerar relatório de status                                                │         │
│  └───────────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                                   │
│                                    │ 10. Dados dos Relatórios                          │
│                                    ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐            │
│  │  P6: AUTENTICAÇÃO E AUTORIZAÇÃO                                        │            │
│  │  ─────────────────────────────                                        │            │
│  │  • Registrar usuário                                                    │            │
│  │  • Login/Logout                                                        │            │
│  │  • Controle de permissões                                              │            │
│  └─────────────────────────────────────────────────────────────────────────┘            │
│                                    │                                                   │
│                                    ▼                                                   │
│  ┌────────────────────────────────┐                                                   │
│  │     ARMAZENAMENTO:             │                                                   │
│  │     USUÁRIOS                   │                                                   │
│  │     ──────────                 │                                                   │
│  │     • id                       │                                                   │
│  │     • username                 │                                                   │
│  │     • password                 │                                                   │
│  │     • is_staff                 │                                                   │
│  └────────────────────────────────┘                                                   │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Descrição dos Elementos

### Entidades Externas

| Entidade | Descrição | Dados Enviados/Recebidos |
|----------|-----------|--------------------------|
| **Cliente** | Cliente do salão que agenda serviços | Dados pessoais, solicitação de agendamento |
| **Profissional** | Profissional que realiza os serviços | Dados profissionais |
| **Administrador** | Gerenciador do sistema | Comandos de gestão, solicitações de relatório |

### Processos

| Processo | Descrição | Entradas | Saídas |
|----------|-----------|----------|--------|
| **P1: Gerenciamento de Clientes** | CRUD de clientes | Dados do cliente | Dados do cliente, confirmação |
| **P2: Gerenciamento de Agendamentos** | CRUD e controle de status | Dados de agendamento, solicitações | Dados do agendamento, confirmação |
| **P3: Gerenciamento de Serviços** | CRUD de serviços | Dados do serviço | Dados do serviço, confirmação |
| **P4: Gerenciamento de Profissionais** | CRUD de profissionais | Dados do profissional | Dados do profissional, confirmação |
| **P5: Gerenciamento de Relatórios** | Geração de relatórios | Parâmetros de filtro | Dados estatísticos |
| **P6: Autenticação e Autorização** | Controle de acesso | Credenciais | Token de autenticação |

### Armazenamentos de Dados

| Armazenamento | Descrição | Dados Armazenados |
|---------------|------------|-------------------|
| **CLIENTES** | Cadastro de clientes | id, nome, email, telefone |
| **SERVIÇOS** | Catálogo de serviços | id, nome, preco, duracao |
| **PROFISSIONAIS** | Cadastro de profissionais | id, nome, especialidade |
| **AGENDAMENTOS** | Registro de agendamentos | id, cliente_id, servico_id, profissional_id, data_hora, status |
| **USUÁRIOS** | Usuários do sistema | id, username, password, is_staff |

### Fluxos de Dados

| Fluxo | Descrição | Origem → Destino |
|-------|-----------|------------------|
| 1 | Dados do Cliente | Cliente → P1 |
| 2 | Dados do Cliente (confirmação) | P1 → CLIENTES |
| 3 | Dados de Agendamento | P1 → P2 |
| 4 | Solicitação de Agendamento | Cliente → P2 |
| 5 | Dados do Serviço | Serviço → P3 |
| 6 | Dados do Serviço | P3 → SERVIÇOS |
| 7 | Dados do Profissional | P4 → PROFISSIONAIS |
| 8 | Solicitações de Relatório | Administrador → P5 |
| 9 | Comandos de Gerenciamento | Administrador → P1, P3, P4 |
| 10 | Dados dos Relatórios | P5 → Administrador |

---

## Diagrama de Fluxo de Dados - Detalhado (Nível 2)

### P2: Gerenciamento de Agendamentos

```
┌─────────────────────────────────────────────────────────────────────┐
│              P2: GERENCIAMENTO DE AGENDAMENTOS                      │
│                                                                      │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│   │  Listar     │     │  Criar      │     │  Editar     │          │
│   │Agendamentos │     │Agendamento  │     │Agendamento  │          │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘          │
│          │                  │                  │                   │
│          └──────────────────┼──────────────────┘                   │
│                             │                                       │
│                             ▼                                       │
│                    ┌────────────────┐                               │
│                    │    VALIDAR     │                               │
│                    │  AGENDAMENTO   │                               │
│                    └────────┬───────┘                               │
│                             │                                       │
│                             ▼                                       │
│                    ┌────────────────┐                               │
│                    │  ATUALIZAR     │──────► Status:               │
│                    │    STATUS      │       AGENDADO/CONCLUIDO/    │
│                    └────────────────┘       CANCELADO               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Regras de Negócio (como Fluxo de Dados)

| Regra | Descrição | Fluxo Associado |
|-------|-----------|-----------------|
| RN1 | Um agendamento deve ter um cliente válido | P1 → P2 |
| RN2 | Um agendamento deve ter um serviço existente | P3 → P2 |
| RN3 | Um agendamento deve ter um profissional disponível | P4 → P2 |
| RN4 | O status pode ser alterado apenas por usuários autenticados | P6 → P2 |
| RN5 | Relatórios só podem ser gerados por administradores | P6 → P5 |

---

## Casos de Uso - Fluxo de Dados

### Caso de Uso 1: Criar Agendamento

```
Cliente ──(1) Dados do Cliente────────────────► P1 ──(2) Confirmação ──► Cliente
                                                      │
                                                      ▼
                                              CLIENTES (armazena)
                                                      │
                                                      ▼
                               ┌───────────────────────────────┐
                               │   P2: Gerenciamento de        │
                               │   Agendamentos                │
                               │                               │
                               │  (3) Dados de Agendamento      │
                               │  ┌─────────────────────┐      │
                               │  │• cliente_id         │      │
                               │  │• servico_id         │      │
                               │  │• profissional_id    │      │
                               │  │• data_hora          │      │
                               │  │• status: AGENDADO   │      │
                               │  └─────────────────────┘      │
                               │              │                 │
                               │              ▼                 │
                               │  ┌─────────────────────┐      │
                               │  │ Validar Agendamento │      │
                               │  └─────────────────────┘      │
                               │              │                 │
                               │              ▼                 │
                               │  ┌─────────────────────┐      │
                               │  │ Armazenar            │      │
                               │  │ Agendamento          │      │
                               │  └─────────────────────┘      │
                               └───────────────────────────────┘
                                              │
                                              ▼
                                      AGENDAMENTOS
```

### Caso de Uso 2: Gerar Relatório de Faturamento

```
Administrador ──(1) Solicitar Relatório───► P5 ──(2) Buscar Dados ──► AGENDAMENTOS
      │                                          │                              │
      │                                          │                              │
      │                                          ▼                              │
      │                                 ┌────────────────┐                     │
      │                                 │  Filtrar por   │                     │
      │                                 │  Status =      │                     │
      │                                 │  CONCLUIDO     │                     │
      │                                 └────────────────┘                     │
      │                                          │                              │
      │                                          ▼                              │
      │                                 ┌────────────────┐                     │
      │                                 │  Calcular      │                     │
      │                                 │  Faturamento   │                     │
      │                                 └────────────────┘                     │
      │                                          │                              │
      │                                          ▼                              │
      │                                 ┌────────────────┐                     │
      │                                 │  Agrupar por   │                     │
      │                                 │  dia/mês       │                     │
      │                                 └────────────────┘                     │
      │                                          │                              │
      │(3) Relatório ◄──────────────────────────┘                              │
      │                                                                         
      ▼                                                                         
(Gráficos/Tabela)
```

---

## Resumo dos Fluxos

| # | Fluxo | Tipo |
|---|-------|------|
| 1 | Cliente → P1 (Dados do Cliente) | Dados |
| 2 | P1 → CLIENTES (Confirmação) | Dados |
| 3 | P1 → P2 (Dados do Cliente para Agendamento) | Dados |
| 4 | Cliente → P2 (Solicitação de Agendamento) | Dados |
| 5 | Serviço → P3 (Dados do Serviço) | Dados |
| 6 | P3 → SERVIÇOS (Confirmação) | Dados |
| 7 | P4 → PROFISSIONAIS (Confirmação) | Dados |
| 8 | Administrador → P5 (Solicitação de Relatório) | Dados |
| 9 | Administrador → Processos (Comandos de Gestão) | Controle |
| 10 | P5 → Administrador (Dados do Relatório) | Dados |
| 11 | Cliente → P6 (Credenciais) | Dados |
| 12 | P6 → USUÁRIOS (Validação) | Dados |

---

## Conclusão

Este documento apresenta a arquitetura de fluxo de dados do Sistema de Agendamentos de Salão. O DFD demonstra como as informações fluem entre os diferentes componentes do sistema, desde a entrada de dados até a geração de relatórios, garantindo uma compreensão clara da arquitetura do sistema.

---

*Documento gerado para o Sistema de Gerenciamento de Agendamentos de Salão*
*Versão: 1.0*

