"""
Views para o app core.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Imovel, Cliente
from .forms import ClienteForm, ImovelForm


def home(request):
    """Página inicial pública."""
    return render(request, 'core/home.html')


def dashboard(request):
    """Dashboard do cliente (rota sensível - HTTPS)."""
    if 'cliente_id' not in request.session:
        messages.error(request, 'Você precisa estar logado para acessar o dashboard.')
        return redirect('login')
    
    try:
        cliente_id = request.session.get('cliente_id')
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        request.session.flush()
        return redirect('login')
    
    # Estatísticas
    total_imoveis = Imovel.objects.count()
    imoveis_ativos = Imovel.objects.filter(ativo=True).count()
    total_clientes = Cliente.objects.count()
    
    # Imóveis recentes
    imoveis_recentes = Imovel.objects.filter(ativo=True).order_by('-data_cadastro')[:5]
    
    # Clientes recentes
    clientes_recentes = Cliente.objects.all().order_by('-data_cadastro')[:5]
    
    context = {
        'cliente': cliente,
        'total_imoveis': total_imoveis,
        'imoveis_ativos': imoveis_ativos,
        'total_clientes': total_clientes,
        'imoveis_recentes': imoveis_recentes,
        'clientes_recentes': clientes_recentes,
    }
    
    return render(request, 'core/dashboard.html', context)


def lista_imoveis(request):
    """Listagem pública de imóveis."""
    imoveis = Imovel.objects.filter(ativo=True).order_by('-data_cadastro')
    context = {
        'imoveis': imoveis
    }
    return render(request, 'core/imoveis_list.html', context)


def contato(request):
    """Página de contato pública."""
    return render(request, 'core/contato.html')


def login_view(request):
    """View de login (rota sensível - HTTPS)."""
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')
        
        # Remove formatação do CPF
        cpf_limpo = ''.join(filter(str.isdigit, cpf)) if cpf else ''
        
        cliente = authenticate(request, cpf=cpf_limpo, password=password)
        if cliente is not None:
            # Armazena o ID do cliente na sessão
            request.session['cliente_id'] = cliente.id
            request.session['cliente_nome'] = cliente.nome
            request.session['cliente_cpf'] = cliente.cpf
            request.session.set_expiry(86400)  # Sessão expira em 24 horas
            messages.success(request, f'Bem-vindo, {cliente.nome}!')
            return redirect('home')
        else:
            messages.error(request, 'CPF ou senha inválidos.')
    return render(request, 'core/login.html')


def logout_view(request):
    """View de logout (rota sensível - HTTPS)."""
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
        del request.session['cliente_nome']
        del request.session['cliente_cpf']
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')


class CadastroClienteView(CreateView):
    """View para cadastro de cliente (rota sensível - HTTPS)."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/cadastro_cliente.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)


class CadastroImovelView(CreateView):
    """View para cadastro de imóvel (rota sensível - HTTPS)."""
    model = Imovel
    form_class = ImovelForm
    template_name = 'core/cadastro_imovel.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Imóvel cadastrado com sucesso!')
        return super().form_valid(form)

