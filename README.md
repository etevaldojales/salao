# Sistema de Gerenciamento de Agendamentos de Salão

## Visão Geral

Este é um sistema de gerenciamento de agendamentos para salões de beleza, desenvolvido em Django. O sistema permite gerenciar clientes, serviços, profissionais e agendamentos, além de fornecer relatórios detalhados sobre o desempenho do salão.

## Tecnologias Utilizadas

- **Backend**: Django 5.0+
- **Database**: MySQL (com suporte a soft delete)
- **Authentication**: Django Authentication System
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Deployment**: Docker

## Funcionalidades

### 1. Autenticação de Usuários

- Registro de novos usuários
- Login/Logout
- Controle de acesso baseado em permissões

### 2. Gerenciamento de Clientes

- Listar clientes cadastrados
- Criar novos clientes (nome, email, telefone)
- Editar informações do cliente
- Excluir clientes (os dados não são removidos permanentemente, permitindo recuperação)

### 3. Gerenciamento de Serviços

- Listar serviços disponíveis
- Criar novos serviços (nome, preço)
- Editar informações do serviço
- Excluir serviços (os dados não são removidos permanentemente, permitindo recuperação)

### 4. Gerenciamento de Profissionais

- Listar profissionais cadastrados
- Criar novos profissionais (nome, especialidade)
- Editar informações do profissional
- Excluir profissionais (os dados não são removidos permanentemente, permitindo recuperação)

### 5. Agendamentos

- Criar novos agendamentos
- Listar todos os agendamentos
- Editar agendamentos existentes
- Status: Agendado, Concluído, Cancelado

### 6. Relatórios

- **Relatório Geral**: Agendamentos por dia
- **Faturamento**: Receita por dia/mês
- **Serviços Populares**: Serviços mais utilizados
- **Desempenho de Profissionais**: Quantidade de atendimentos por profissional
- **Status**: Distribuição de agendamentos por status
- **Clientes Top**: Top 10 clientes que mais gastaram

### 7. Gerenciamento de Usuários (Admin)

- Listar usuários do sistema
- Editar permissões de usuários
- Acesso restrito a administradores

## Instalação

### Pré-requisitos

- Python 3.10+
- MySQL
- Docker (opcional)

### Configuração Local

1. **Criar e ativar ambiente virtual:**

```bash
py -m venv venv
# Windows
.\venv\Scripts\activate.ps1
# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

3. **Configurar banco de dados:**

Edite o arquivo `projeto/settings.py` com as configurações do seu banco de dados MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'salao_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. **Executar migrações:**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Criar super usuário:**

```bash
python manage.py createsuperuser
```

6. **Iniciar servidor:**

```bash
python manage.py runserver
```

### Configuração com Docker

```bash
docker-compose up --build
```

## Estrutura do Projeto

```
salao/
├── projeto/                  # Configurações do Django
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # WSGI config
├── agendamentos/            # App principal
│   ├── models.py            # Modelos de banco de dados
│   ├── views.py             # Lógica de negócio
│   ├── forms.py             # Formulários
│   ├── urls.py              # URLs do app
│   └── templates/           # Templates HTML
│       ├── base.html        # Template base
│       ├── index.html       # Página inicial
│       ├── cliente_*.html   # Templates de cliente
│       ├── servico_*.html   # Templates de serviço
│       ├── profissional_*.html  # Templates de profissional
│       ├── relatorios.html  # Página de relatórios
│       └── ...
├── docker-compose.yml       # Configuração Docker
├── Dockerfile               # Dockerfile
├── requirements.txt         # Dependências Python
└── manage.py                # Script de gerenciamento Django
```

## Modelos de Dados

### Cliente
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | PK automático |
| nome | Char(100) | Nome do cliente |
| email | Email | Email (opcional) |
| telefone | Char(20) | Telefone de contato |

### Servico
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | PK automático |
| nome | Char(100) | Nome do serviço |
| preco | Decimal(8,2) | Preço do serviço |

### Profissional
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | PK automático |
| nome | Char(100) | Nome do profissional |
| especialidade | Char(100) | Especialidade |

### Agendamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | PK automático |
| cliente | ForeignKey | Cliente relacionado |
| servico | ForeignKey | Serviço realizado |
| profissional | ForeignKey | Profissional responsável |
| data_hora | DateTime | Data e hora do agendamento |
| status | Char(15) | Status (AGENDADO, CONCLUIDO, CANCELADO) |

## URLs do Sistema

| URL | Descrição |
|-----|-----------|
| `/` | Página inicial (listagem de agendamentos) |
| `/novo/` | Criar novo agendamento |
| `/editar/<id>/` | Editar agendamento |
| `/clientes/` | Listar clientes |
| `/clientes/novo/` | Criar cliente |
| `/clientes/editar/<id>/` | Editar cliente |
| `/clientes/excluir/<id>/` | Excluir cliente |
| `/servicos/` | Listar serviços |
| `/servicos/novo/` | Criar serviço |
| `/servicos/editar/<id>/` | Editar serviço |
| `/servicos/excluir/<id>/` | Excluir serviço |
| `/profissionais/` | Listar profissionais |
| `/profissionais/novo/` | Criar profissional |
| `/profissionais/editar/<id>/` | Editar profissional |
| `/profissionais/excluir/<id>/` | Excluir profissional |
| `/relatorios/` | Página de relatórios |
| `/usuarios/` | Gerenciar usuários (admin) |
| `/register/` | Registro de novos usuários |
| `/login/` | Login de usuários |
| `/logout/` | Logout de usuários |

## API de Relatórios

O sistema oferece endpoints JSON para integração com gráficos e dashboards:

| Endpoint | Descrição |
|----------|-----------|
| `/relatorios/dados/` | Agendamentos concluídos por dia |
| `/relatorios/faturamento/?periodo=dia\|mes` | Faturamento por período |
| `/relatorios/servicos/` | Serviços mais populares |
| `/relatorios/profissionais/` | Desempenho de profissionais |
| `/relatorios/status/` | Distribuição por status |
| `/relatorios/clientes/` | Top 10 clientes |

## Screenshots

O sistema inclui:
- Interface responsiva com Bootstrap
- Dashboard de agendamentos
- Formulários de CRUD para todas as entidades
- Gráficos interativos para relatórios
- Tabelas com paginação

## Contribuição

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Este projeto está sob a licença MIT.

## Autor

Desenvolvido para fins educacionais e de demonstração.

