from django.db import models
from django.utils import timezone
from decimal import Decimal


class Cliente(models.Model):
    """Modelo para cadastro de clientes"""
    nome = models.CharField('Nome', max_length=200)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20, blank=True)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True)
    endereco = models.TextField('Endereço', blank=True)
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def saldo_devedor(self):
        """Retorna o saldo devedor do cliente (crediário)"""
        total = self.ordens.filter(
            tipo_pagamento='CREDIARIO',
            status__in=['ABERTA', 'FINALIZADA']
        ).aggregate(
            total=models.Sum('valor_total')
        )['total'] or Decimal('0.00')
        
        pagamentos = self.pagamentos.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')
        
        return total - pagamentos


class OrdemServico(models.Model):
    """Modelo para ordens de serviço"""
    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    TIPO_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('PIX', 'PIX'),
        ('CREDIARIO', 'Crediário (Fiado)'),
    ]

    numero = models.CharField('Número OS', max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ordens', verbose_name='Cliente')
    veiculo = models.CharField('Veículo', max_length=200, blank=True)
    placa = models.CharField('Placa', max_length=20, blank=True)
    km = models.CharField('KM', max_length=20, blank=True)
    
    defeito_reclamado = models.TextField('Defeito Reclamado', blank=True)
    observacoes = models.TextField('Observações', blank=True)
    
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ABERTA')
    tipo_pagamento = models.CharField('Tipo de Pagamento', max_length=20, choices=TIPO_PAGAMENTO_CHOICES, default='DINHEIRO')
    
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2, default=0)
    
    data_abertura = models.DateTimeField('Data de Abertura', default=timezone.now)
    data_finalizacao = models.DateTimeField('Data de Finalização', null=True, blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_abertura']

    def __str__(self):
        return f"OS {self.numero} - {self.cliente.nome}"

    def calcular_total(self):
        """Calcula o valor total da OS baseado nos serviços e produtos"""
        total_servicos = self.servicos.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')
        
        total_produtos = self.produtos.aggregate(
            total=models.Sum('valor_total')
        )['total'] or Decimal('0.00')
        
        return total_servicos + total_produtos

    def save(self, *args, **kwargs):
        # Gera número da OS se não existir
        if not self.numero:
            ultimo = OrdemServico.objects.order_by('-id').first()
            if ultimo:
                ultimo_numero = int(ultimo.numero)
                self.numero = str(ultimo_numero + 1).zfill(6)
            else:
                self.numero = '000001'
        
        # Atualiza valor total
        if self.pk:
            self.valor_total = self.calcular_total()
        
        super().save(*args, **kwargs)


class ServicoOS(models.Model):
    """Modelo para serviços de uma ordem de serviço"""
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos')
    descricao = models.TextField('Descrição do Serviço')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f"{self.descricao[:50]} - R$ {self.valor}"


class ProdutoOS(models.Model):
    """Modelo para produtos de uma ordem de serviço"""
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='produtos')
    descricao = models.TextField('Descrição do Produto')
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=2, default=1)
    valor_unitario = models.DecimalField('Valor Unitário', max_digits=10, decimal_places=2)
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f"{self.descricao[:50]} - R$ {self.valor_total}"

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)


class PagamentoCrediario(models.Model):
    """Modelo para controle de pagamentos do crediário"""
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pagamentos')
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.PROTECT, related_name='pagamentos', null=True, blank=True)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField('Data do Pagamento', default=timezone.now)
    observacoes = models.TextField('Observações', blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento Crediário'
        verbose_name_plural = 'Pagamentos Crediário'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"R$ {self.valor} - {self.cliente.nome} - {self.data_pagamento.strftime('%d/%m/%Y')}"
