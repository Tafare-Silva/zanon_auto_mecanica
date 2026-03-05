from django.contrib import admin
from .models import Cliente, OrdemServico, ServicoOS, ProdutoOS, PagamentoCrediario


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'criado_em']
    search_fields = ['nome', 'cpf_cnpj', 'telefone', 'email']
    list_filter = ['criado_em']


class ServicoOSInline(admin.TabularInline):
    model = ServicoOS
    extra = 1


class ProdutoOSInline(admin.TabularInline):
    model = ProdutoOS
    extra = 1


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'status', 'tipo_pagamento', 'valor_total', 'data_abertura']
    search_fields = ['numero', 'cliente__nome', 'veiculo', 'placa']
    list_filter = ['status', 'tipo_pagamento', 'data_abertura']
    inlines = [ServicoOSInline, ProdutoOSInline]


@admin.register(PagamentoCrediario)
class PagamentoCrediarioAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'valor', 'data_pagamento', 'ordem_servico']
    search_fields = ['cliente__nome']
    list_filter = ['data_pagamento']
