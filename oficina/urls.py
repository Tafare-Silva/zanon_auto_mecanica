from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    
    # Clientes
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_criar, name='cliente_criar'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/deletar/', views.cliente_deletar, name='cliente_deletar'),
    
    # Ordens de Serviço
    path('ordens/', views.os_lista, name='os_lista'),
    path('ordens/nova/', views.os_criar, name='os_criar'),
    path('ordens/<int:pk>/', views.os_detalhe, name='os_detalhe'),
    path('ordens/<int:pk>/editar/', views.os_editar, name='os_editar'),
    path('ordens/<int:pk>/deletar/', views.os_deletar, name='os_deletar'),
    path('ordens/<int:pk>/imprimir/', views.os_imprimir, name='os_imprimir'),
    
    # Serviços
    path('ordens/<int:os_pk>/servico/adicionar/', views.servico_adicionar, name='servico_adicionar'),
    path('servicos/<int:pk>/deletar/', views.servico_deletar, name='servico_deletar'),
    
    # Produtos
    path('ordens/<int:os_pk>/produto/adicionar/', views.produto_adicionar, name='produto_adicionar'),
    path('produtos/<int:pk>/deletar/', views.produto_deletar, name='produto_deletar'),
    
    # Crediário
    path('crediario/', views.crediario_lista, name='crediario_lista'),
    path('crediario/<int:cliente_pk>/pagamento/', views.pagamento_adicionar, name='pagamento_adicionar'),
    path('pagamentos/<int:pk>/deletar/', views.pagamento_deletar, name='pagamento_deletar'),
    
    # AJAX
    path('ajax/cliente/criar/', views.cliente_criar_ajax, name='cliente_criar_ajax'),
]
