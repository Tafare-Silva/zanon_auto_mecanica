# 📁 Estrutura de Settings (Configurações)

Este projeto utiliza **múltiplos arquivos de configuração** para separar ambientes de desenvolvimento e produção.

## 📂 Estrutura

```
core/
└── settings/
    ├── __init__.py      # Carrega automaticamente o settings correto
    ├── base.py          # Configurações compartilhadas
    ├── development.py   # Configurações de desenvolvimento
    └── production.py    # Configurações de produção
```

---

## 🔧 Como Usar

### **Desenvolvimento Local (Padrão)**

Por padrão, o projeto roda em modo **desenvolvimento**.

```bash
# Simplesmente rode:
python manage.py runserver

# Usa automaticamente: core.settings.development
```

**Características do ambiente de desenvolvimento:**
- ✅ DEBUG = True
- ✅ SQLite (banco mais simples)
- ✅ ALLOWED_HOSTS = ['*']
- ✅ SECRET_KEY fixa (não segura, mas OK para dev)
- ✅ Emails aparecem no console

---

### **Produção**

Para rodar em modo **produção**:

```bash
# Opção 1: Via variável de ambiente
export DJANGO_ENVIRONMENT=production
python manage.py runserver

# Opção 2: Especificar diretamente o settings
python manage.py runserver --settings=core.settings.production

# Opção 3: Configurar no .env ou servidor
DJANGO_ENVIRONMENT=production gunicorn core.wsgi:application
```

**Características do ambiente de produção:**
- ✅ DEBUG = False
- ✅ PostgreSQL (via variáveis de ambiente)
- ✅ ALLOWED_HOSTS configurável
- ✅ SECRET_KEY via .env (segura)
- ✅ HTTPS forçado
- ✅ Configurações de segurança ativadas
- ✅ Logging para arquivo

---

## 📝 Arquivos de Configuração

### **base.py** - Configurações Compartilhadas
Tudo que é comum entre desenvolvimento e produção:
- Apps instaladas
- Middleware
- Templates
- Internacionalização
- Arquivos estáticos

### **development.py** - Desenvolvimento
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# SQLite (mais simples)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### **production.py** - Produção
```python
from .base import *
from decouple import config

DEBUG = False
SECRET_KEY = config('SECRET_KEY')  # Via .env
ALLOWED_HOSTS = config('ALLOWED_HOSTS')

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        # ... outras configs via .env
    }
}

# Segurança HTTPS
SECURE_SSL_REDIRECT = True
# ... outras configs de segurança
```

---

## 🔐 Variáveis de Ambiente (.env)

Para **produção**, crie um arquivo `.env` na raiz do projeto:

```bash
# .env (APENAS PRODUÇÃO)
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com

DB_NAME=oficina_db
DB_USER=oficina_user
DB_PASSWORD=senha-super-segura
DB_HOST=localhost
DB_PORT=5432
```

**⚠️ IMPORTANTE:** Nunca comite o arquivo `.env` no Git!

---

## 🚀 Deploy (Produção)

### **1. No servidor, configure o ambiente:**

```bash
# Criar arquivo .env
nano .env
# Cole as variáveis de produção

# Configurar variável de ambiente
export DJANGO_ENVIRONMENT=production
```

### **2. Adicionar ao systemd/supervisor:**

```ini
# supervisor.conf
[program:oficina]
environment=DJANGO_ENVIRONMENT=production
command=/path/to/venv/bin/gunicorn core.wsgi:application
```

### **3. Ou configurar no gunicorn_config.py:**

```python
# gunicorn_config.py
import os
os.environ['DJANGO_ENVIRONMENT'] = 'production'
```

---

## 🛠️ Comandos Úteis

### **Ver qual settings está sendo usado:**
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.DATABASES)
```

### **Rodar com settings específico:**
```bash
# Desenvolvimento
python manage.py runserver --settings=core.settings.development

# Produção
python manage.py runserver --settings=core.settings.production
```

### **Migrations em produção:**
```bash
DJANGO_ENVIRONMENT=production python manage.py migrate
```

---

## 📊 Comparação

| Configuração | Desenvolvimento | Produção |
|--------------|----------------|----------|
| **DEBUG** | True | False |
| **Banco** | SQLite | PostgreSQL |
| **SECRET_KEY** | Fixa no código | Via .env |
| **ALLOWED_HOSTS** | ['*'] | Configurável |
| **HTTPS** | Não | Forçado |
| **Logs** | Console | Arquivo + Console |
| **Email** | Console | SMTP |

---

## 💡 Dicas

### **Adicionar nova configuração:**

1. Se for **comum** (dev e prod): adicione em `base.py`
2. Se for **apenas dev**: adicione em `development.py`
3. Se for **apenas prod**: adicione em `production.py`

### **Usar PostgreSQL em desenvolvimento:**

Edite `development.py` e descomente a seção PostgreSQL:

```python
# development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oficina_db_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **Debug em produção (temporariamente):**

```bash
# NO ARQUIVO .env
DEBUG=True  # Apenas para debug, volte para False depois!
```

---

## ✅ Benefícios desta Estrutura

- ✅ **Separação clara** entre dev e prod
- ✅ **Não precisa alterar código** para deploy
- ✅ **Mais seguro** - secrets não ficam no código
- ✅ **Flexível** - fácil adicionar novos ambientes (staging, testing)
- ✅ **Padrão Django** - segue boas práticas da comunidade

---

## 🆘 Solução de Problemas

### **Erro: No module named 'decouple'**
```bash
pip install python-decouple
```

### **Erro em produção: KeyError 'SECRET_KEY'**
```bash
# Você esqueceu de criar o arquivo .env
# Crie o arquivo .env com todas as variáveis necessárias
```

### **Quero ver qual settings está carregado:**
```python
# manage.py shell
from django.conf import settings
print(settings.DEBUG)
```

---

**Estrutura profissional, fácil de manter e segura!** 🚀
