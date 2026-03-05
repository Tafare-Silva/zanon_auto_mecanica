# Sistema de Gestão para Oficina Mecânica

Sistema completo de gerenciamento de ordens de serviço para oficina mecânica desenvolvido com Django, PostgreSQL e Tailwind CSS.

## 🚀 Funcionalidades

- ✅ **Cadastro de Clientes** - Gerenciar informações dos clientes
- ✅ **Ordens de Serviço** - Criar, editar e visualizar OS
- ✅ **Serviços e Produtos** - Campos livres para digitação (sem necessidade de cadastro prévio)
- ✅ **Tipos de Pagamento** - Dinheiro, cartão, PIX e crediário
- ✅ **Controle de Crediário** - Gerenciar pagamentos a prazo (fiado)
- ✅ **Impressão de OS** - Imprimir ou salvar em PDF
- ✅ **Dashboard** - Visão geral com estatísticas
- ✅ **Design Moderno** - Interface responsiva com Tailwind CSS

## 📋 Requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone ou extraia o projeto

```bash
cd oficina_mecanica
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o PostgreSQL

Crie um banco de dados PostgreSQL:

```sql
CREATE DATABASE oficina_db;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE oficina_db TO postgres;
```

Se você usar credenciais diferentes, edite o arquivo `core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seu_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário (para acessar o admin)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar seu usuário administrador.

### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse o sistema em: **http://localhost:8000**

## 🎯 Como Usar

### Dashboard
- Acesse a página inicial para ver estatísticas gerais
- Visualize total de clientes, OS abertas e valor em crediário

### Cadastrar Cliente
1. Clique em "Clientes" no menu
2. Clique em "Novo Cliente"
3. Preencha os dados e salve

### Criar Ordem de Serviço
1. Clique em "Nova OS" (botão verde no canto superior)
2. Selecione o cliente
3. Preencha dados do veículo (opcional)
4. Descreva o defeito reclamado
5. Escolha o tipo de pagamento
6. Clique em "Salvar"

### Adicionar Serviços e Produtos
1. Após criar a OS, você será direcionado para a tela de edição
2. Clique em "Adicionar Serviço" para incluir serviços
   - Digite a descrição livremente (sem necessidade de cadastro prévio)
   - Informe o valor
3. Clique em "Adicionar Produto" para incluir peças
   - Digite a descrição livremente
   - Informe quantidade e valor unitário
4. O valor total será calculado automaticamente

### Imprimir/Salvar PDF
1. Acesse a OS desejada
2. Clique em "Imprimir"
3. Use Ctrl+P (ou Cmd+P no Mac)
4. Escolha "Salvar como PDF" como impressora de destino
5. Salve o arquivo

### Gerenciar Crediário
1. Clique em "Crediário" no menu
2. Visualize clientes com saldo devedor
3. Clique em "Registrar Pagamento" para lançar um pagamento
4. O saldo é atualizado automaticamente

## 🎨 Personalização

### Alterar informações da oficina
Edite o arquivo `templates/os_imprimir.html` e modifique o cabeçalho:

```html
<h1 class="text-3xl font-bold text-gray-800 mb-2">SUA OFICINA</h1>
<p class="text-gray-600">Seu endereço aqui</p>
<p class="text-gray-600">Telefone: (00) 0000-0000</p>
<p class="text-gray-600">Email: seu@email.com</p>
```

### Cores e estilo
O sistema usa Tailwind CSS. Para alterar cores, edite as classes nos templates:

- `bg-blue-600` - Cor de fundo azul
- `text-blue-600` - Texto azul
- `hover:bg-blue-700` - Cor ao passar o mouse

Cores disponíveis: blue, green, red, yellow, purple, gray, etc.

## 📊 Estrutura do Projeto

```
oficina_mecanica/
├── core/               # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── oficina/            # App principal
│   ├── models.py       # Modelos de dados
│   ├── views.py        # Lógica de negócio
│   ├── forms.py        # Formulários
│   ├── urls.py         # Rotas
│   └── admin.py        # Painel administrativo
├── templates/          # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── cliente_*.html
│   ├── os_*.html
│   └── ...
├── static/             # Arquivos estáticos
├── media/              # Uploads
├── manage.py           # Gerenciador Django
└── requirements.txt    # Dependências
```

## 🔒 Segurança

⚠️ **IMPORTANTE para produção:**

1. Altere a `SECRET_KEY` em `core/settings.py`
2. Configure `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use variáveis de ambiente para senhas
5. Configure HTTPS
6. Faça backup regular do banco de dados

## 🐛 Resolução de Problemas

### Erro de conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme usuário, senha e nome do banco em `settings.py`

### Erro ao instalar psycopg2
No Linux, instale as dependências:
```bash
sudo apt-get install python3-dev libpq-dev
```

### Erro de migração
```bash
python manage.py makemigrations --empty oficina
python manage.py migrate
```

## 📝 Licença

Este projeto é livre para uso pessoal e comercial.

## 👨‍💻 Suporte

Para dúvidas ou problemas, revise este README ou a documentação do Django em https://docs.djangoproject.com/

---

**Desenvolvido com Django + PostgreSQL + Tailwind CSS**
