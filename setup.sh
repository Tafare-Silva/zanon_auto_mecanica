#!/bin/bash

echo "=========================================="
echo "Sistema de Gestão - Oficina Mecânica"
echo "=========================================="
echo ""

# Verificar se o venv existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -q -r requirements.txt

# Executar migrações
echo "Executando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "=========================================="
echo "✓ Instalação concluída com sucesso!"
echo "=========================================="
echo ""
echo "Para iniciar o servidor, execute:"
echo "  python manage.py runserver"
echo ""
echo "Depois acesse: http://localhost:8000"
echo ""
echo "Para criar um superusuário (admin):"
echo "  python manage.py createsuperuser"
echo ""
