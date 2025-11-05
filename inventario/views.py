from django.shortcuts import render, redirect
from .models import Produto, LimiteProduto
from .forms import ProdutoForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

def registrar(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro bem-sucedido. Agora você pode fazer o login.')
            return redirect('inventario:login')
    else:
        form = RegistrationForm()
    return render(request, 'inventario/registrar.html', {'form': form})

def logout_view(request):
    ''' Faz logout do usuário e redireciona para a página de login '''
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('inventario:login')

@login_required
def home(request):
    lista_produtos = Produto.objects.filter(ativo=True, deletado_em__isnull=True).order_by('nome')
    
    # Paginação
    itens_por_pagina = request.GET.get('itens_por_pagina', 10)
    paginator = Paginator(lista_produtos, itens_por_pagina)
    pagina = request.GET.get('pagina')
    produtos = paginator.get_page(pagina)
    
    for produto in produtos:
        try:
            limite = produto.limite
            status = limite.get_status(produto.quantidade_atual)
            produto.limite_minimo = limite.limite_minimo
            produto.limite_ideal = limite.limite_ideal
        except LimiteProduto.DoesNotExist:
            status = 'Sem limite definido'
        produto.status = status
    
    contexto = {'produtos': produtos, 'itens_por_pagina': itens_por_pagina}
    
    return render(request, 'inventario/home.html', contexto)

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.quantidade_atual = 0
            produto.save()
            messages.success(request, 'Produto criado com sucesso.')
            return redirect('inventario:home')
        else:
            messages.error(request, f'Por favor, corrija os erros abaixo: {form.errors}')
    else:
        form = ProdutoForm()
    return render(request, 'inventario/criar_produto.html', {'form': form})