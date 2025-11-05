from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Produto, LimiteProduto, MovimentoEstoque
from .forms import CategoriaForm, ProdutoForm, LimiteProdutoForm, MovimentoEstoqueForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
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