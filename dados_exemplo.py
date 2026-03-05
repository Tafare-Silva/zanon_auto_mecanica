# Script para popular banco de dados com dados de exemplo
# Execute: python manage.py shell < dados_exemplo.py

from oficina.models import Cliente, OrdemServico, ServicoOS, ProdutoOS
from decimal import Decimal

# Criar clientes de exemplo
print("Criando clientes de exemplo...")

clientes = [
    Cliente.objects.create(
        nome="João Silva",
        cpf_cnpj="123.456.789-00",
        telefone="(11) 98765-4321",
        email="joao@email.com",
        endereco="Rua das Flores, 123"
    ),
    Cliente.objects.create(
        nome="Maria Santos",
        cpf_cnpj="987.654.321-00",
        telefone="(11) 91234-5678",
        email="maria@email.com",
        endereco="Av. Principal, 456"
    ),
    Cliente.objects.create(
        nome="Pedro Oliveira",
        telefone="(11) 99999-8888",
        endereco="Rua do Comércio, 789"
    ),
]

print(f"✓ {len(clientes)} clientes criados")

# Criar ordens de serviço
print("\nCriando ordens de serviço...")

os1 = OrdemServico.objects.create(
    cliente=clientes[0],
    veiculo="Fiat Uno 2015",
    placa="ABC-1234",
    km="85000",
    defeito_reclamado="Motor fazendo barulho estranho e perdendo potência",
    tipo_pagamento="DINHEIRO",
    status="EM_ANDAMENTO"
)

os2 = OrdemServico.objects.create(
    cliente=clientes[1],
    veiculo="Volkswagen Gol 2018",
    placa="XYZ-5678",
    km="45000",
    defeito_reclamado="Freios rangendo",
    tipo_pagamento="CARTAO_CREDITO",
    status="ABERTA"
)

os3 = OrdemServico.objects.create(
    cliente=clientes[2],
    veiculo="Chevrolet Onix 2020",
    placa="DEF-9012",
    km="25000",
    defeito_reclamado="Revisão periódica",
    tipo_pagamento="CREDIARIO",
    status="ABERTA"
)

print("✓ 3 ordens de serviço criadas")

# Adicionar serviços
print("\nAdicionando serviços...")

ServicoOS.objects.create(
    ordem_servico=os1,
    descricao="Troca de correia dentada",
    valor=Decimal("450.00")
)
ServicoOS.objects.create(
    ordem_servico=os1,
    descricao="Regulagem de motor",
    valor=Decimal("280.00")
)

ServicoOS.objects.create(
    ordem_servico=os2,
    descricao="Troca de pastilhas de freio dianteiras",
    valor=Decimal("320.00")
)
ServicoOS.objects.create(
    ordem_servico=os2,
    descricao="Sangria do sistema de freios",
    valor=Decimal("80.00")
)

ServicoOS.objects.create(
    ordem_servico=os3,
    descricao="Troca de óleo e filtro",
    valor=Decimal("150.00")
)
ServicoOS.objects.create(
    ordem_servico=os3,
    descricao="Alinhamento e balanceamento",
    valor=Decimal("120.00")
)

print("✓ Serviços adicionados")

# Adicionar produtos
print("\nAdicionando produtos...")

ProdutoOS.objects.create(
    ordem_servico=os1,
    descricao="Correia dentada original",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("180.00")
)
ProdutoOS.objects.create(
    ordem_servico=os1,
    descricao="Tensor da correia",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("95.00")
)

ProdutoOS.objects.create(
    ordem_servico=os2,
    descricao="Jogo de pastilhas de freio",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("220.00")
)
ProdutoOS.objects.create(
    ordem_servico=os2,
    descricao="Fluido de freio DOT 4",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("45.00")
)

ProdutoOS.objects.create(
    ordem_servico=os3,
    descricao="Óleo sintético 5W30",
    quantidade=Decimal("4"),
    valor_unitario=Decimal("35.00")
)
ProdutoOS.objects.create(
    ordem_servico=os3,
    descricao="Filtro de óleo",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("28.00")
)
ProdutoOS.objects.create(
    ordem_servico=os3,
    descricao="Filtro de ar",
    quantidade=Decimal("1"),
    valor_unitario=Decimal("42.00")
)

print("✓ Produtos adicionados")

# Atualizar valores totais
print("\nAtualizando valores totais...")
for os in [os1, os2, os3]:
    os.valor_total = os.calcular_total()
    os.save()

print("✓ Valores atualizados")

print("\n" + "="*50)
print("DADOS DE EXEMPLO CRIADOS COM SUCESSO!")
print("="*50)
print(f"\nClientes: {Cliente.objects.count()}")
print(f"Ordens de Serviço: {OrdemServico.objects.count()}")
print(f"Serviços: {ServicoOS.objects.count()}")
print(f"Produtos: {ProdutoOS.objects.count()}")
print("\nAcesse http://localhost:8000 para ver os dados!")
