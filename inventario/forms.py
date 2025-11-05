from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Produto, LimiteProduto, MovimentoEstoque

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("nome", "email", "senha", "confirmacao_senha")

class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Categoria'})
    )
    
    ativo = forms.BooleanField(attrs={'class': 'form-check-input'}, required=False)
    
    class Meta:
        model = Categoria
        fields = ['nome', 'ativo']
        
class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'})
    )
    
    sku = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU do Produto'}),
        required=False
    )
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Produto', 'rows': 3}),
        required=False
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    quantidade_atual = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade Atual'})
    )
    
    ativo = forms.BooleanField(attrs={'class': 'form-check-input'}, required=False)
    
    class Meta:
        model = Produto
        fields = ['nome', 'sku', 'descricao', 'categoria', 'quantidade_atual', 'ativo']

class LimiteProdutoForm(forms.ModelForm):
    limite_minimo = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limite Mínimo'})
    )
    
    limite_ideal = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limite Ideal'})
    )
    
    tipo_limite = forms.ChoiceField(
        choices=LimiteProduto.TIPOS_LIMITE,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = LimiteProduto
        fields = ['limite_minimo', 'limite_ideal', 'tipo_limite']

class MovimentoEstoqueForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo_movimento = forms.ChoiceField(
        choices=MovimentoEstoque.TIPOS_MOVIMENTO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
    )
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Movimento', 'rows': 3}),
        required=False
    )
    
    class Meta:
        model = MovimentoEstoque
        fields = ['produto', 'tipo_movimento', 'quantidade']