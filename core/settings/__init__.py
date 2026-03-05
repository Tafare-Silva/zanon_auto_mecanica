"""
Settings Package
Carrega automaticamente o settings correto baseado na variável DJANGO_SETTINGS_MODULE
ou usa development como padrão
"""

import os

# Detectar ambiente
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *

# Permitir que usuário avançado sobrescreva via variável de ambiente
# Exemplo: export DJANGO_SETTINGS_MODULE=core.settings.production
