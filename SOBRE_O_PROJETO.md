# 🚗 SISTEMA DE GESTÃO PARA OFICINA MECÂNICA

## 📦 O QUE VOCÊ RECEBEU

Uma aplicação web completa e moderna para gerenciar sua oficina mecânica, desenvolvida com:
- **Django 5.0** (Framework Python)
- **PostgreSQL** (Banco de dados)
- **Tailwind CSS** (Design moderno e responsivo)

## ✨ FUNCIONALIDADES COMPLETAS

### 1. Gestão de Clientes
- ✅ Cadastro completo com telefone, email, endereço
- ✅ CPF/CNPJ opcional
- ✅ Histórico de serviços por cliente
- ✅ Controle de saldo devedor

### 2. Ordens de Serviço
- ✅ Numeração automática sequencial
- ✅ Dados do veículo (modelo, placa, KM)
- ✅ Descrição livre do defeito reclamado
- ✅ Status: Aberta, Em Andamento, Finalizada, Cancelada
- ✅ Múltiplos tipos de pagamento

### 3. Serviços (Campos Livres)
- ✅ **SEM necessidade de cadastro prévio**
- ✅ Digite livremente a descrição do serviço
- ✅ Informe o valor
- ✅ Adicione quantos serviços precisar

### 4. Produtos (Campos Livres)
- ✅ **SEM necessidade de cadastro prévio**
- ✅ Digite livremente a descrição do produto
- ✅ Informe quantidade e valor unitário
- ✅ Cálculo automático do total

### 5. Formas de Pagamento
- ✅ Dinheiro
- ✅ Cartão de Crédito
- ✅ Cartão de Débito
- ✅ PIX
- ✅ **Crediário (Fiado)**

### 6. Controle de Crediário
- ✅ Visualização de todos os clientes com dívidas
- ✅ Saldo devedor atualizado automaticamente
- ✅ Registro de pagamentos parciais
- ✅ Histórico completo de pagamentos
- ✅ Vinculação de pagamentos a OS específicas

### 7. Impressão e PDF
- ✅ Layout profissional para impressão
- ✅ Salvar como PDF direto do navegador (Ctrl+P → Salvar como PDF)
- ✅ Dados completos: cliente, veículo, serviços, produtos
- ✅ Espaço para assinaturas

### 8. Dashboard Intuitivo
- ✅ Total de clientes cadastrados
- ✅ OS abertas e em andamento
- ✅ Total em crediário
- ✅ Últimas ordens criadas
- ✅ Ações rápidas

## 🎨 DESIGN MODERNO

- Interface limpa e profissional
- Cores suaves e agradáveis
- Ícones ilustrativos (Font Awesome)
- Responsivo (funciona em celular, tablet e desktop)
- Mensagens de sucesso/erro elegantes
- Botões com efeitos hover
- Tabelas organizadas e legíveis

## 📁 ESTRUTURA DO PROJETO

```
oficina_mecanica/
├── README.md              # Documentação completa
├── GUIA_RAPIDO.md        # Guia de início rápido
├── requirements.txt       # Dependências Python
├── manage.py             # Gerenciador Django
├── setup.sh              # Script de instalação (Linux/Mac)
├── dados_exemplo.py      # Dados para teste
│
├── core/                 # Configurações do projeto
│   ├── settings.py       # Configurações gerais
│   ├── urls.py          # Rotas principais
│   └── wsgi.py          # Servidor WSGI
│
├── oficina/             # Aplicação principal
│   ├── models.py        # Modelos de dados (banco)
│   ├── views.py         # Lógica de negócio
│   ├── forms.py         # Formulários
│   ├── urls.py          # Rotas da aplicação
│   └── admin.py         # Painel administrativo
│
└── templates/           # Templates HTML (16 arquivos)
    ├── base.html        # Template base
    ├── index.html       # Dashboard
    ├── cliente_*.html   # Telas de clientes
    ├── os_*.html        # Telas de ordens
    ├── servico_*.html   # Telas de serviços
    ├── produto_*.html   # Telas de produtos
    └── crediario_*.html # Telas de crediário
```

## 🚀 INSTALAÇÃO RÁPIDA

### Passo 1: Instalar Requisitos
```bash
# Python 3.8+
# PostgreSQL 12+
```

### Passo 2: Criar Banco de Dados
```sql
CREATE DATABASE oficina_db;
```

### Passo 3: Instalar e Configurar
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Passo 4: Iniciar
```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

## 📝 EXEMPLO DE USO

### Cenário 1: Cliente traz carro para revisão
1. Cadastre o cliente (se novo)
2. Crie uma nova OS
3. Adicione serviços livremente:
   - "Troca de óleo e filtro - R$ 150,00"
   - "Alinhamento e balanceamento - R$ 120,00"
4. Adicione produtos livremente:
   - "Óleo sintético 5W30 - 4 litros - R$ 35,00/un"
   - "Filtro de óleo - 1 unidade - R$ 28,00/un"
5. Sistema calcula total automaticamente
6. Escolha forma de pagamento
7. Imprima ou salve em PDF

### Cenário 2: Cliente quer pagar depois (fiado)
1. Ao criar OS, selecione "Crediário (Fiado)"
2. O valor fica registrado como pendente
3. Quando cliente pagar:
   - Acesse "Crediário" no menu
   - Clique em "Registrar Pagamento"
   - Informe valor e data
4. Saldo é atualizado automaticamente

## 🎯 DIFERENCIAIS

### ✅ Campos Livres (Principal Requisito)
- **Serviços**: Digite qualquer descrição, sem cadastro prévio
- **Produtos**: Digite qualquer descrição, sem cadastro prévio
- Máxima flexibilidade para o dia a dia da oficina

### ✅ Controle de Crediário Completo
- Visualização clara de quem deve
- Registro fácil de pagamentos
- Histórico detalhado
- Atualização automática de saldos

### ✅ Impressão Profissional
- Layout pronto para impressão
- Salvamento direto em PDF
- Espaços para assinaturas
- Dados completos e organizados

### ✅ Interface Intuitiva
- Não precisa de manual
- Tudo onde você espera encontrar
- Feedback visual de todas as ações
- Design limpo e moderno

## 🔧 PERSONALIZAÇÃO

Fácil de personalizar! Alguns exemplos:

### Alterar nome da oficina no cabeçalho
Edite `templates/os_imprimir.html`, linha ~8

### Mudar cores
Edite as classes Tailwind nos templates:
- `bg-blue-600` → `bg-green-600` (fundo verde)
- `text-blue-600` → `text-purple-600` (texto roxo)

### Adicionar campos
Edite `oficina/models.py` e execute:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📊 BANCO DE DADOS

### Tabelas Criadas
- **Cliente** - Dados dos clientes
- **OrdemServico** - Ordens de serviço
- **ServicoOS** - Serviços por OS
- **ProdutoOS** - Produtos por OS
- **PagamentoCrediario** - Pagamentos do crediário

### Relacionamentos
- Cliente → pode ter várias OS
- OS → pode ter vários serviços
- OS → pode ter vários produtos
- Cliente → pode ter vários pagamentos

## 🛡️ SEGURANÇA

Para produção (uso real):
1. Altere `SECRET_KEY` em `core/settings.py`
2. Configure `DEBUG = False`
3. Use HTTPS
4. Configure backup automático do banco
5. Use variáveis de ambiente para senhas

## 💡 DICAS

### Para melhor desempenho:
- Use PostgreSQL (não SQLite) em produção
- Faça backup diário do banco
- Mantenha Python e dependências atualizados

### Para organização:
- Crie uma OS para cada serviço
- Use observações para detalhes importantes
- Mantenha cadastro de clientes atualizado

### Para crediário:
- Registre pagamentos logo que receber
- Revise saldos semanalmente
- Use observações em pagamentos

## 📞 RECURSOS ADICIONAIS

- **Django Docs**: https://docs.djangoproject.com/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **PostgreSQL**: https://www.postgresql.org/docs/

## ✅ CHECKLIST DE FUNCIONALIDADES

- [x] Cadastro de clientes
- [x] Criação de ordens de serviço
- [x] Campos livres para serviços
- [x] Campos livres para produtos
- [x] Múltiplas formas de pagamento
- [x] Controle de crediário (fiado)
- [x] Registro de pagamentos
- [x] Impressão de OS
- [x] Salvamento em PDF
- [x] Dashboard com estatísticas
- [x] Design moderno e responsivo
- [x] Cálculo automático de totais
- [x] Interface intuitiva

## 🎉 PRONTO PARA USO!

O sistema está **100% funcional** e pronto para uso imediato. Basta seguir as instruções de instalação no `README.md` ou `GUIA_RAPIDO.md`.

---

**Desenvolvido com ❤️ usando Django + PostgreSQL + Tailwind CSS**

*Sistema completo, moderno e fácil de usar para gestão de oficinas mecânicas*
