from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST
from decimal import Decimal
import json
from .models import Cliente, OrdemServico, ServicoOS, ProdutoOS, PagamentoCrediario
from .forms import ClienteForm, OrdemServicoForm, ServicoOSForm, ProdutoOSForm, PagamentoCrediarioForm


# Views principais
def index(request):
    """Dashboard principal"""
    total_clientes = Cliente.objects.count()
    os_abertas = OrdemServico.objects.filter(status='ABERTA').count()
    os_em_andamento = OrdemServico.objects.filter(status='EM_ANDAMENTO').count()
    
    # Calcular total em crediário
    clientes_crediario = Cliente.objects.all()
    total_crediario = sum([c.saldo_devedor() for c in clientes_crediario])
    
    # Últimas ordens de serviço
    ultimas_os = OrdemServico.objects.all()[:10]
    
    context = {
        'total_clientes': total_clientes,
        'os_abertas': os_abertas,
        'os_em_andamento': os_em_andamento,
        'total_crediario': total_crediario,
        'ultimas_os': ultimas_os,
    }
    return render(request, 'index.html', context)


# Views de Cliente
def cliente_lista(request):
    """Lista de clientes"""
    clientes = Cliente.objects.all()
    
    # Adicionar saldo devedor para cada cliente
    for cliente in clientes:
        cliente.saldo = cliente.saldo_devedor()
    
    return render(request, 'cliente_lista.html', {'clientes': clientes})


def cliente_criar(request):
    """Criar novo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    
    return render(request, 'cliente_form.html', {'form': form, 'titulo': 'Novo Cliente'})


def cliente_editar(request, pk):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})


def cliente_deletar(request, pk):
    """Deletar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente deletado com sucesso!')
        return redirect('cliente_lista')
    
    return render(request, 'cliente_deletar.html', {'cliente': cliente})


# Views de Ordem de Serviço
def os_lista(request):
    """Lista de ordens de serviço"""
    ordens = OrdemServico.objects.all()
    return render(request, 'os_lista.html', {'ordens': ordens})


def os_criar(request):
    """Criar nova ordem de serviço"""
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os = form.save()
            messages.success(request, f'Ordem de Serviço {os.numero} criada com sucesso!')
            return redirect('os_editar', pk=os.pk)
    else:
        form = OrdemServicoForm()
    
    return render(request, 'os_form.html', {'form': form, 'titulo': 'Nova Ordem de Serviço'})


def os_editar(request, pk):
    """Editar ordem de serviço"""
    os = get_object_or_404(OrdemServico, pk=pk)
    
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=os)
        if form.is_valid():
            form.save()
            # Recalcular total
            os.valor_total = os.calcular_total()
            os.save()
            messages.success(request, 'Ordem de Serviço atualizada com sucesso!')
            return redirect('os_detalhe', pk=os.pk)
    else:
        form = OrdemServicoForm(instance=os)
    
    return render(request, 'os_editar.html', {
        'form': form,
        'os': os,
        'servicos': os.servicos.all(),
        'produtos': os.produtos.all(),
    })


def os_detalhe(request, pk):
    """Detalhes da ordem de serviço"""
    os = get_object_or_404(OrdemServico, pk=pk)
    return render(request, 'os_detalhe.html', {
        'os': os,
        'servicos': os.servicos.all(),
        'produtos': os.produtos.all(),
    })


def os_deletar(request, pk):
    """Deletar ordem de serviço"""
    os = get_object_or_404(OrdemServico, pk=pk)
    
    if request.method == 'POST':
        numero = os.numero
        os.delete()
        messages.success(request, f'Ordem de Serviço {numero} deletada com sucesso!')
        return redirect('os_lista')
    
    return render(request, 'os_deletar.html', {'os': os})


def os_imprimir(request, pk):
    """Imprimir ordem de serviço"""
    os = get_object_or_404(OrdemServico, pk=pk)
    servicos = os.servicos.all()
    produtos = os.produtos.all()
    
    # Calcular totais separados
    total_servicos = sum([s.valor for s in servicos]) if servicos else Decimal('0.00')
    total_produtos = sum([p.valor_total for p in produtos]) if produtos else Decimal('0.00')
    
    return render(request, 'os_imprimir.html', {
        'os': os,
        'servicos': servicos,
        'produtos': produtos,
        'total_servicos': total_servicos,
        'total_produtos': total_produtos,
    })


# Views de Serviço
def servico_adicionar(request, os_pk):
    """Adicionar serviço à OS"""
    os = get_object_or_404(OrdemServico, pk=os_pk)
    
    if request.method == 'POST':
        # Verificar se os dados vêm do formulário inline
        if 'descricao' in request.POST and 'valor' in request.POST:
            try:
                ServicoOS.objects.create(
                    ordem_servico=os,
                    descricao=request.POST.get('descricao'),
                    valor=Decimal(request.POST.get('valor'))
                )
                # Atualizar valor total da OS
                os.valor_total = os.calcular_total()
                os.save()
                messages.success(request, 'Serviço adicionado com sucesso!')
                return redirect('os_editar', pk=os.pk)
            except (ValueError, TypeError) as e:
                messages.error(request, f'Erro ao adicionar serviço: valor inválido')
                return redirect('os_editar', pk=os.pk)
        else:
            form = ServicoOSForm(request.POST)
            if form.is_valid():
                servico = form.save(commit=False)
                servico.ordem_servico = os
                servico.save()
                
                # Atualizar valor total da OS
                os.valor_total = os.calcular_total()
                os.save()
                
                messages.success(request, 'Serviço adicionado com sucesso!')
                return redirect('os_editar', pk=os.pk)
    else:
        form = ServicoOSForm()
    
    return render(request, 'servico_form.html', {'form': form, 'os': os})


def servico_deletar(request, pk):
    """Deletar serviço"""
    servico = get_object_or_404(ServicoOS, pk=pk)
    os = servico.ordem_servico
    
    servico.delete()
    
    # Atualizar valor total da OS
    os.valor_total = os.calcular_total()
    os.save()
    
    messages.success(request, 'Serviço removido com sucesso!')
    return redirect('os_editar', pk=os.pk)


# Views de Produto
def produto_adicionar(request, os_pk):
    """Adicionar produto à OS"""
    os = get_object_or_404(OrdemServico, pk=os_pk)
    
    if request.method == 'POST':
        # Verificar se os dados vêm do formulário inline
        if 'descricao' in request.POST and 'quantidade' in request.POST and 'valor_unitario' in request.POST:
            try:
                ProdutoOS.objects.create(
                    ordem_servico=os,
                    descricao=request.POST.get('descricao'),
                    quantidade=Decimal(request.POST.get('quantidade')),
                    valor_unitario=Decimal(request.POST.get('valor_unitario'))
                )
                # Atualizar valor total da OS
                os.valor_total = os.calcular_total()
                os.save()
                messages.success(request, 'Produto adicionado com sucesso!')
                return redirect('os_editar', pk=os.pk)
            except (ValueError, TypeError) as e:
                messages.error(request, f'Erro ao adicionar produto: valores inválidos')
                return redirect('os_editar', pk=os.pk)
        else:
            form = ProdutoOSForm(request.POST)
            if form.is_valid():
                produto = form.save(commit=False)
                produto.ordem_servico = os
                produto.save()
                
                # Atualizar valor total da OS
                os.valor_total = os.calcular_total()
                os.save()
                
                messages.success(request, 'Produto adicionado com sucesso!')
                return redirect('os_editar', pk=os.pk)
    else:
        form = ProdutoOSForm()
    
    return render(request, 'produto_form.html', {'form': form, 'os': os})


def produto_deletar(request, pk):
    """Deletar produto"""
    produto = get_object_or_404(ProdutoOS, pk=pk)
    os = produto.ordem_servico
    
    produto.delete()
    
    # Atualizar valor total da OS
    os.valor_total = os.calcular_total()
    os.save()
    
    messages.success(request, 'Produto removido com sucesso!')
    return redirect('os_editar', pk=os.pk)


# Views de Crediário
def crediario_lista(request):
    """Lista de clientes com crediário"""
    clientes = Cliente.objects.all()
    
    clientes_com_divida = []
    for cliente in clientes:
        saldo = cliente.saldo_devedor()
        if saldo > 0:
            clientes_com_divida.append({
                'cliente': cliente,
                'saldo': saldo,
                'ordens': cliente.ordens.filter(tipo_pagamento='CREDIARIO', status__in=['ABERTA', 'FINALIZADA']),
                'pagamentos': cliente.pagamentos.all()[:5]
            })
    
    return render(request, 'crediario_lista.html', {'clientes_com_divida': clientes_com_divida})


def pagamento_adicionar(request, cliente_pk):
    """Adicionar pagamento de crediário"""
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    if request.method == 'POST':
        form = PagamentoCrediarioForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.cliente = cliente
            pagamento.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('crediario_lista')
    else:
        form = PagamentoCrediarioForm(initial={'cliente': cliente})
        # Filtrar apenas OS do cliente com crediário
        form.fields['ordem_servico'].queryset = OrdemServico.objects.filter(
            cliente=cliente,
            tipo_pagamento='CREDIARIO'
        )
    
    return render(request, 'pagamento_form.html', {'form': form, 'cliente': cliente})


def pagamento_deletar(request, pk):
    """Deletar pagamento"""
    pagamento = get_object_or_404(PagamentoCrediario, pk=pk)
    
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Pagamento removido com sucesso!')
        return redirect('crediario_lista')
    
    return render(request, 'pagamento_deletar.html', {'pagamento': pagamento})


# View AJAX para criar cliente
@require_POST
def cliente_criar_ajax(request):
    """Criar cliente via AJAX"""
    try:
        data = json.loads(request.body)
        
        cliente = Cliente.objects.create(
            nome=data.get('nome'),
            cpf_cnpj=data.get('cpf_cnpj', ''),
            telefone=data.get('telefone'),
            email=data.get('email', ''),
            endereco=data.get('endereco', ''),
            observacoes=data.get('observacoes', '')
        )
        
        return JsonResponse({
            'success': True,
            'cliente_id': cliente.id,
            'cliente_nome': cliente.nome
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
