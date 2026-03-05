# GUIA RÁPIDO DE INÍCIO

## Passo 1: Instalar PostgreSQL

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Windows:
Baixe e instale de: https://www.postgresql.org/download/windows/

### Mac:
```bash
brew install postgresql
brew services start postgresql
```

## Passo 2: Criar o Banco de Dados

```bash
# Acessar o PostgreSQL
sudo -u postgres psql

# Executar os comandos SQL:
CREATE DATABASE oficina_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE oficina_db TO postgres;
\q
```

## Passo 3: Configurar o Projeto

```bash
# Instalar Python 3.8+ se necessário
python --version  # ou python3 --version

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Passo 4: Preparar o Banco

```bash
# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (opcional, para acessar /admin)
python manage.py createsuperuser
```

## Passo 5: Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Resumo dos Comandos

```bash
# Iniciar servidor
python manage.py runserver

# Parar servidor
Ctrl + C

# Acessar admin
http://localhost:8000/admin

# Aplicar mudanças no banco
python manage.py makemigrations
python manage.py migrate
```

## Primeiro Uso

1. Acesse http://localhost:8000
2. Cadastre um cliente em "Clientes" > "Novo Cliente"
3. Crie uma OS em "Nova OS" (botão verde)
4. Adicione serviços e produtos livremente
5. Imprima a OS ou salve em PDF

## Problemas Comuns

### PostgreSQL não conecta
- Verifique se está rodando: `sudo systemctl status postgresql`
- Confira usuário/senha em `core/settings.py`

### Erro ao instalar psycopg2
- Linux: `sudo apt install python3-dev libpq-dev`
- Mac: `brew install postgresql`
- Windows: Use `psycopg2-binary`

### Porta 8000 em uso
```bash
python manage.py runserver 8080
```

---

Pronto! Agora você tem um sistema completo de gestão para oficina mecânica! 🚗🔧
